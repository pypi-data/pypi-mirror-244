import logging

from langchain.chains import LLMChain
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, ConversationalAgent
from langchain.schema import OutputParserException

from cmysql.config import AGENT_VERBOSE

from cmysql.tools import CHAT_LLM
from cmysql.ai.generator import ai_generate
from cmysql.ai.agent_prompts import (
    PROMPT_AGENT_PREFIX,
    PROMPT_AGENT_SUFFIX,
    PROMPT_AGENT_FORMAT_INSTRUCTIONS,
)
from cmysql.ai.prompts import (
    GENERATE_MDATAKG_CHANGES_PROMPT,
    GENERATE_SQL_PROMPT,
    GENERATE_ANSWER_PROMPT,
)
from cmysql.ai.graph_and_vector import MDataKG
from cmysql.ai.mysql_database import MySQLDatabase
from cmysql.logs import log


class SQLDataAgent(object):
    def __init__(self):
        self.llm = CHAT_LLM
        self.global_chain = LLMChain(llm=self.llm, prompt=self.global_prompt)
        self.global_agent = ConversationalAgent(
            llm_chain=self.global_chain,
            tools=self.tools
        )
        self.global_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent = AgentExecutor.from_agent_and_tools(
            agent=self.global_agent,
            tools=self.tools,
            memory=self.global_memory,
            verbose=AGENT_VERBOSE
        )

    @property
    def global_prompt(self):
        return ConversationalAgent.create_prompt(
            self.tools,
            prefix=PROMPT_AGENT_PREFIX,
            suffix=PROMPT_AGENT_SUFFIX,
            format_instructions=PROMPT_AGENT_FORMAT_INSTRUCTIONS,
        )

    @property
    def tools(self):
        return [
            Tool.from_function(
                func=self.tool_modify_mdatakg,
                name="Edit Meta Data",
                description="用于更新表名、表描述、列名、列描述，或者列与列之间的关系。",
            ),
            Tool.from_function(
                func=self.tool_qa,
                name="Answer Question",
                description="根据Question，寻找相关的表，并利用表结构生成SQL，然后执行SQL获取数据，最后生成答案。",
            ),
            Tool.from_function(
                func=self.tool_exec_sql,
                name="Exec SQL",
                description="执行SQL查询数据",
            ),
        ]

    def tool_modify_mdatakg(self, question: str):
        kg = MDataKG()
        related_mdata = kg.find(
            question=question,
            table_score_threshold=3.0,
        )
        if not related_mdata:
            return "没有找到相关的表"
        mdatakg_changes = ai_generate(
            GENERATE_MDATAKG_CHANGES_PROMPT,
            user_feedback=question,
            related_mdata=related_mdata,

        )
        _, _, _, _, info = kg.modify(mdatakg_changes)
        return info

    def _check_sql(
        self,
        mdata: dict,
        sql_cmd: str,
    ):
        check_result = ai_generate(
            GENERATE_SQL_PROMPT,
            output_format="str",
            mdata=mdata,
            sql_cmd=sql_cmd,
        )
        return check_result == 'valid'

    def _gen_and_exe_sql(
            self,
            question: str,
            mdata: dict,
    ) -> (str, list):
        _max_retry = 5
        for _ in range(_max_retry):
            sql_cmd = ai_generate(
                GENERATE_SQL_PROMPT,
                question=question,
                mdata=mdata,
            )["SQL"]
            if self._check_sql(mdata, sql_cmd):
                log.info(f"生成的SQL语句为：{sql_cmd}, 符合要求。")

                try:
                    sql_result = MySQLDatabase().retrieve_data(sql_cmd)
                    log.info(f"使用SQL语句：{sql_cmd[:20]}...，查询到了{len(sql_result)}条数据。")
                    return sql_cmd, sql_result
                except Exception as e:
                    log.info(f"执行SQL语句 {sql_cmd} 时出错，尝试重新生成。")
            else:
                log.info(f"生成的SQL语句：{sql_cmd}，不符合要求，尝试重新生成。")

        err_msg = f"重试{_max_retry}次后，仍然无法生成符合要求的SQL语句，请检查问题描述是否有误。"
        log.error(err_msg)
        raise Exception(err_msg)

    def _gen_answer_from_sql_result(
            self,
            question: str,
            mdata: dict,
            sql_cmd: str,
            sql_result: list,
            callbacks: list = None,
    ) -> str:
        sql_result_str = str(sql_result)
        if len(sql_result_str) >= 2000:
            raise Exception(f"数据量过大（共{len(sql_result_str)}字），请缩小查询范围。")

        answer = ai_generate(
            GENERATE_ANSWER_PROMPT,
            question=question,
            mdata=mdata,
            sql_cmd=sql_cmd,
            sql_result=sql_result_str,
        )
        return answer

    def tool_qa(self, question: str):
        kg = MDataKG()
        related_mdata = kg.find(question)

        log.info(f"开始回答问题：{question}")
        log.info(f"使用的Meta Data为：{related_mdata}")

        try:
            sql_cmd, sql_result = self._gen_and_exe_sql(question, related_mdata)
            answer = self._gen_answer_from_sql_result(
                question,
                related_mdata,
                sql_cmd,
                sql_result,
            )
            return answer
        except Exception as e:
            return str(e)

    def tool_exec_sql(self, sql: str):
        sql_result = MySQLDatabase().retrieve_data(sql)
        return str(sql_result)
