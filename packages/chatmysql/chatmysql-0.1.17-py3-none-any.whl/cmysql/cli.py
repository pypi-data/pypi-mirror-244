import subprocess
import sys
import os
import pty

import select
import readline
import time
import json

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from cmysql.logs import log, plog
from cmysql.metabrain import init_brain
from cmysql.ai.agent import SQLDataAgent, OutputParserException
from cmysql.tools import extract_and_save_mysql_args
from cmysql.exceptions import MDataKGInitError


def identify_intent(question):
    # 使用简化的意图识别。实际上可能需要更复杂的逻辑或NLP模型。
    if question.lower().strip().startswith(("select", "update", "insert", "delete", "create", "alter",
                                    "drop", "show", "desc", "use", "set", "grant",
                                    "revoke", "begin", "commit", "rollback", "call",
                                    "truncate", "explain", "lock", "unlock", "rename",
                                    "load", "replace", "reload", "flush", "optimize",
                                    "repair", "check", "analyze", "delimiter")):
        return "SQL_COMMAND"
    else:
        return "CHAT"


########################  以下是增加对 DELIMITER 的支持的代码 #######################
DELIMITER = ';'  # Default delimiter
SECONDARY_DELIMITER = '\g'  # Secondary delimiter


def is_command_complete(command, delimiter):
    """Check if the command is complete based on the current delimiter."""
    if command.strip().endswith(delimiter) or command.strip().endswith(SECONDARY_DELIMITER):
        return True
    else:
        return False


def extract_and_set_delimiter(command):
    """Extract delimiter from a command and set it as the current delimiter."""
    global DELIMITER
    prefix = "delimiter"
    if command.lower().startswith(prefix):
        DELIMITER = command[len(prefix):].strip()
        return True
    return False

######################################################################


LONG_TIMEOUT = 3600  # 1 hour in seconds
SHORT_TIMEOUT = 0.5


def main():
    # 在程序开始前检查用户是否同意将数据上传到云端（提供中英文提示）
    consent = input("您同意将表结构（不含数据）上传到云端吗？(是/否)。 \n"
                    "Do you agree to upload table definition(without data) to the cloud? (yes(y)/no): ")
    if consent.lower() not in ['yes', 'y', '是']:
        print("用户未同意。程序退出。User did not agree. Exiting the program.")
        sys.exit(0)

    # 获取命令行参数
    args = sys.argv[1:]
    mysql_cli_cmd = ['mysql'] + args
    extract_and_save_mysql_args(args)

    # 解决从 subprocess.Popen() 调用mysql获取stdout和stderr时的阻塞问题
    # 使用pty（伪终端）来模拟终端行为，从而使mysql CLI认为它正在与实际终端交互，这样它可能会更积极地刷新其输出。
    master, slave = pty.openpty()
    # 使用pty来启动mysql CLI
    process = subprocess.Popen(mysql_cli_cmd, stdin=slave, stdout=slave, stderr=slave, text=True, close_fds=True)

    plog.info("Welcome to cmysql, type 'exit' or use Ctrl-D to quit.\n")
    # 获取运行mysql cli之后的第一次输出
    first_output_lines = []
    while True:
        rlist, _, _ = select.select([master], [], [], 0.3)
        if rlist:
            output = os.read(master, 1024).decode('utf-8')
            if output.strip().startswith("Type 'help;'"):
                continue
            if output.strip().startswith("mysql>"):
                continue
            first_output_lines += output
        else:
            break
    plog.info("".join(first_output_lines))

    init_brain()
    sql_agent = SQLDataAgent()

    while True:
        try:
            agent_input = input("cmysql> ")
        except EOFError:  # 使用 Ctrl-D 退出
            break

        if agent_input.lower() == 'exit':
            break

        # 如果输入是空的（只按了回车键），则继续
        if not agent_input.strip():
            continue

        # 将命令添加到历史中
        readline.add_history(agent_input)

        intent = identify_intent(agent_input)

        if intent == "SQL_COMMAND":

            # 如果用户尝试设置一个新的定界符
            if extract_and_set_delimiter(agent_input):
                print(f"Delimiter set to {DELIMITER}")
                continue

            # 检查是否输入了完整的命令
            while not is_command_complete(agent_input, DELIMITER):
                try:
                    next_line = input("    -> ")  # 使用稍微不同的提示符，表示这是命令的延续
                    agent_input += f"\n{next_line}"  # 添加到当前命令
                except EOFError:
                    break

            os.write(master, (agent_input + "\n").encode('utf-8'))
            response_lines = []
            current_timeout = LONG_TIMEOUT  # start with long timeout
            start_time = time.time()  # start timer for the long timeout
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time > LONG_TIMEOUT:
                    plog.warning("Command timed out after waiting for 1 hour!")
                    break

                # 在大多数情况下，使用process.stderr.readline()时，如果没有任何输出，它会阻塞。
                # 解决此问题的一个方法是设置非阻塞读取或使用线程。但为了简化，我们可以使用select模块来检查是否有可用的输出。
                rlist, _, _ = select.select([master], [], [], current_timeout)
                if rlist:
                    output = os.read(master, 1024).decode('utf-8')
                    if output:
                        response_lines.append(output)
                        current_timeout = SHORT_TIMEOUT  # switch to short timeout after getting some output

                        # Check if the command has completed
                        end_texts = ["rows in set", "row in set", "ERROR", "Database changed"]
                        if any(text in output for text in end_texts):
                            break

                else:
                    # If we have received some data but not all, then continue waiting with short timeout.
                    if response_lines:
                        continue
                    # Otherwise, no more data to read, possibly long command
                    break

            # Filter out the echo of the command and the "mysql> " prompt
            filtered_output = "\n".join([line for line in "".join(response_lines).split("\n") if
                                         line.strip() != agent_input.strip() and not line.strip().startswith("mysql> ")])
            plog.info("\n" + filtered_output.strip())
        elif intent == "CHAT":
            with sql_agent.llm.get_callback() as cb:
                try:
                    output = json.loads(sql_agent.agent.run(agent_input))
                    answer = output["HumanLikeAnswer"]
                    sqls = output["StructureQueries"]
                    plog.info(answer + '\n')
                    # 打印每一个SQL，带编号
                    for i, sql in enumerate(sqls):
                        plog.info(f"SQL[{i + 1}]: {sql}")
                except OutputParserException as e:
                    plog.error(e.observation)
                except MDataKGInitError as e:
                    plog.error(e)
                log.debug(f"问题：{agent_input}, 统计：{cb}")


if __name__ == "__main__":
    main()
