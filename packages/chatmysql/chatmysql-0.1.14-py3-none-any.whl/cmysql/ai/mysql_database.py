from pydantic.types import Any, List, Dict, Optional
import sqlalchemy as sa
from sqlalchemy import create_engine, text
import json

from langchain.chains.base import Chain
from langchain.callbacks.manager import CallbackManagerForChainRun
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from cmysql.tools import CHAT_LLM
from cmysql.ai.prompts import GENERATE_SQL_PROMPT, GENERATE_ANSWER_PROMPT, CHECK_SQL_PROMPT
from cmysql.logs import log
from cmysql.config import MySQLConfig as MC


class MData(object):
    pass


class MySQLDatabase(object):

    def __init__(self):
        self.uri = f"mysql+pymysql://{MC.user}:{MC.password}@{MC.host}:{MC.port}"
        self.engine = create_engine(self.uri)

    def retrieve_data(self, sql_cmd: str):
        log.debug(f"执行SQL语句：{sql_cmd}")
        with self.engine.connect() as conn:
            result = conn.execute(text(sql_cmd))
            rows = result.fetchall()
            return rows

    def retrieve_meta_data(self, databases: list[str] = None) -> dict:
        # if databases is None, then fetch all databases.
        insp = sa.inspect(self.engine)
        if not databases:
            databases = insp.get_schema_names()

        result = {"databases": {}}

        db_count = 0
        table_count = 0
        column_count = 0

        for db in databases:
            if db in [
                'information_schema',
                'performance_schema',
                'mysql',
                'sys',
            ]:
                continue

            db_meta_data = result["databases"].setdefault(db, {"tables": {}})
            db_count += 1

            for table_name in insp.get_table_names(schema=db):
                columns = insp.get_columns(table_name, schema=db)

                # Adjusting the column info to match the new structure.
                # _column_info = [f"{column['name']}: {column.get('comment', '')}" for column in columns]
                _column_info = {}
                for column in columns:
                    _column_info[column['name']] = column.get('comment', '')

                table_comment = insp.get_table_comment(table_name, schema=db).get('text', '')
                db_meta_data["tables"][table_name] = {
                    "desc": table_comment,
                    "columns": _column_info
                }
                table_count += 1
                column_count += len(columns)

        log.debug(f"共查到{db_count}个数据库，{table_count}张表，{column_count}个字段。")
        return result

    # def gen_and_exe_sql(self,
    #                     question: str,
    #                     mdata: dict,
    #                     callbacks=None) -> (str, list[Any]):
    #     gen_sql_prompt = PromptTemplate(
    #         input_variables=["question_and_mdata"],
    #         template=GENERATE_SQL_PROMPT,
    #         template_format="jinja2"
    #     )
    #     gen_sql_chain = LLMChain(llm=CHAT_LLM,
    #                              prompt=gen_sql_prompt,
    #                              )
    #     question_and_mdata_str = json.dumps({"question": question, "mdata": mdata})
    #     _max_retry = 5
    #     for _ in range(_max_retry):
    #         sql_cmd = gen_sql_chain.predict(callbacks=callbacks,
    #                                         question_and_mdata=question_and_mdata_str
    #                                         ).strip()
    #         if self.check_sql(mdata, sql_cmd, callbacks=callbacks):
    #             log.info(f"生成的SQL语句为：{sql_cmd}, 符合要求。")
    #
    #             try:
    #                 sql_result = self.retrieve_data(sql_cmd)
    #                 log.info(f"使用SQL语句：{sql_cmd[:20]}...，查询到了{len(sql_result)}条数据。")
    #                 return sql_cmd, sql_result
    #             except Exception as e:
    #                 log.info(f"执行SQL语句 {sql_cmd} 时出错，尝试重新生成。")
    #         else:
    #             log.info(f"生成的SQL语句：{sql_cmd}，不符合要求，尝试重新生成。")
    #
    #     err_msg = f"重试{_max_retry}次后，仍然无法生成符合要求的SQL语句，请检查问题描述是否有误。"
    #     log.error(err_msg)
    #     raise Exception(err_msg)

    # @staticmethod
    # def check_sql(mdata: dict, sql_cmd: str, callbacks=None) -> bool:
    #     check_sql_prompt = PromptTemplate(
    #         input_variables=["mdata", "sql_cmd"],
    #         template=CHECK_SQL_PROMPT,
    #         template_format="jinja2"
    #     )
    #     check_sql_chain = LLMChain(llm=CHAT_LLM,
    #                                prompt=check_sql_prompt,
    #                                )
    #     check_result = check_sql_chain.predict(callbacks=callbacks,
    #                                            mdata=json.dumps(mdata),
    #                                            sql_cmd=sql_cmd,
    #                                            ).strip()
    #     return check_result == 'valid'

    # def qa(self,
    #        question: str,
    #        mdata: dict,
    #        callbacks=None
    #        ) -> str:
    #
    #     log.info(f"开始回答问题：{question}")
    #     log.info(f"使用的Meta Data为：{mdata}")
    #
    #     try:
    #         sql_cmd, sql_result = self.gen_and_exe_sql(question, mdata, callbacks=callbacks)
    #     except Exception as e:
    #         return str(e)
    #
    #     sql_result_str = str(sql_result)
    #     if len(sql_result_str) >= 2000:
    #         raise Exception(f"数据量过大（共{len(sql_result_str)}字），请缩小查询范围。")
    #
    #     gen_answer_prompt = PromptTemplate(
    #         input_variables=["question", "mdata", "sql_cmd", "sql_result"],
    #         template=GENERATE_ANSWER_PROMPT,
    #         template_format="jinja2"
    #     )
    #
    #     gen_answer_chain = LLMChain(llm=CHAT_LLM,
    #                                 prompt=gen_answer_prompt,
    #                                 # verbose=True
    #                                 )
    #     answer = gen_answer_chain.predict(callbacks=callbacks,
    #                                       question=question,
    #                                       mdata=json.dumps(mdata),
    #                                       sql_cmd=sql_cmd,
    #                                       sql_result=sql_result_str
    #                                       ).strip()
    #     return answer

# class QADatabaseChain(Chain):
#     @property
#     def input_keys(self) -> List[str]:
#         return ['question_and_mdata']
#
#     @property
#     def output_keys(self) -> List[str]:
#         return ['answer']
#
#     def _call(self,
#         inputs: Dict[str, Any],
#         run_manager: Optional[CallbackManagerForChainRun] = None,
#     ) -> Dict[str, str]:
#         question_and_mdata = json.loads(inputs[self.input_keys[0]])
#         question = question_and_mdata['question']
#         mdata = question_and_mdata['mdata']
#         answer = MySQLDatabase().qa(
#             question=question,
#             mdata=mdata,
#             callbacks=run_manager.get_child()
#         )
#         return {self.output_keys[0]: answer}

#
# class ExecSQLChain(Chain):
#     input_key: str = 'sql_cmd'
#     output_key: str = 'sql_result'
#
#     @property
#     def input_keys(self) -> List[str]:
#         return [self.input_key]
#
#     @property
#     def output_keys(self) -> List[str]:
#         return [self.output_key]
#
#     def _call(self,
#         inputs: Dict[str, Any],
#         run_manager: Optional[CallbackManagerForChainRun] = None,
#     ) -> Dict[str, str]:
#         sql_result = MySQLDatabase().retrieve_data(inputs[self.input_key])
#         return {self.output_key: str(sql_result)}


if __name__ == "__main__":
    pass

