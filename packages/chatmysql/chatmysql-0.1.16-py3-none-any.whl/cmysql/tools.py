import os
import prettytable
from langchain.embeddings import OpenAIEmbeddings
from langchain.callbacks import get_openai_callback

from pydantic.types import Any, List, Dict, Optional
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import Callbacks, BaseMessage
from langchain.schema import LLMResult
from cmysql.logs import log
from cmysql.config import (OPENAI_API_KEY, OPENAI_PROXY,
                           OPENAI_LLM_VERBOSE, OPENAI_LLM_MODEL_NAME,
                           OPENAI_LLM_TEMPERATURE, OPENAI_LLM_MAX_TOKENS,
                           OPENAI_EMBEDDING_MODEL_NAME, OPENAI_EMBEDDING_VECTOR_SIZE)
from cmysql.config import MySQLConfig


class ChatOpenAIWithLog(ChatOpenAI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openai_api_key = OPENAI_API_KEY
        self.openai_proxy = OPENAI_PROXY

    @property
    def get_callback(self):
        return get_openai_callback

    def generate(
        self,
        messages: List[List[BaseMessage]],
        stop: Optional[List[str]] = None,
        callbacks: Callbacks = None,
        *,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> LLMResult:
        result = super().generate(messages=messages, stop=stop,
                                  callbacks=callbacks, tags=tags, metadata=metadata, **kwargs)
        # log.debug(f"LLM PROMPT: {messages[0][0].content}")
        log.debug(f"LLM COMPLETION: {result.generations[0][0].text}")
        # log.debug(f"LLM SUMMARY: {result.llm_output}")
        return result


CHAT_LLM = ChatOpenAIWithLog(temperature=OPENAI_LLM_TEMPERATURE,
                             model_name=OPENAI_LLM_MODEL_NAME,
                             max_tokens=OPENAI_LLM_MAX_TOKENS,
                             verbose=OPENAI_LLM_VERBOSE
                             )
EMBEDDING_MODEL = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL_NAME)
EMBEDDING_VECTOR_SIZE = OPENAI_EMBEDDING_VECTOR_SIZE


def extract_and_save_mysql_args(args):
    """
    Extracts And Save MySQL related arguments from the command line arguments.
    """

    # 设置默认值
    host = "localhost"
    port = 3306
    user = "root"
    password = ""
    db = ""

    for i, arg in enumerate(args):
        if arg == "--host":
            host = args[i + 1]
        elif arg == "--port":
            port = int(args[i + 1])
        elif arg == "--user":
            user = args[i + 1]
        elif arg == "--password":
            password = args[i + 1]
        elif arg == "--database" or arg == "--db":
            db = args[i + 1]

    MySQLConfig.host = host
    MySQLConfig.port = port
    MySQLConfig.user = user
    MySQLConfig.password = password
    MySQLConfig.db = db

    return {"host": host, "port": port, "user": user, "password": password, "db": db}


def calculate_top_related_tables(similar_search_results: list,
                                 top_n=10,
                                 table_score_threshold=4.0,
                                 db_score_threshold_ratio=0.3,
                                 ) -> list:
    """
    以下是综合相关度的计算公式：

    对于任意列（例如col-i）：
    score_col_i = base_score_col_i * f_column

    对于任意表（例如table-j）：
    score_table_j = base_score_table_j * f_table + sum(score_columns_belonging_to_table_j)

    对于任意数据库（例如db-k）：
    score_db_k = base_score_db_k * f_db + sum(score_tables_belonging_to_db_k)


    其中：
    base_score_col_i 是列col-i的基本相关度。
    base_score_table_j 是表table-j的基本相关度。
    base_score_db_k 是数据库db-k的基本相关度。
    f_column 是列的调整因子。
    f_table 是表的调整因子。
    f_db 是数据库的调整因子。
    score_columns_belonging_to_table_j 是属于table-j的所有列的综合相关度的列表。
    score_tables_belonging_to_db_k 是属于db-k的所有表的综合相关度的列表。


    以下为一个具体的示例：

    通过近似检索到的实体相关度如下：
    table-1: 0.8
        col-1 (属于 table-1): 0.3
    table-2: 0
        col-2 (属于未明确指出的 table-2): 0.8
        col-3 (同样属于 table-2): 0.9

    那么，表的综合相关度为：
    col-1的综合相关度为0.3（0.3*1）
    table-1的综合相关度为1.5（0.8*1.5 + 0.3*1）

    col-2的综合相关度为0.8（0.8*1）
    col-3的综合相关度为0.9（0.9*1）
    table-2的综合相关度为1.7（0*1.5 + 0.8*1 + 0.9*1）

    从结果中可以看出，尽管table-1的基本相关度较高，
    但由于table-2关联的两个列col-2和col-3的总相关度之和较大，使得table-2的综合相关度略高于table-1。
    """
    f_db = 1.8
    f_table = 1.5
    f_column = 1

    # Extract related entities and compute their base scores and type
    base_scores = []
    for result in similar_search_results:
        base_scores.append({
            'entity_name': result['name'],
            'entity_type': result['type'],
            'score': result['score']
        })

    # Calculate table comprehensive scores based on their columns
    table_scores = {}
    db_scores = {}
    for details in base_scores:
        entity = details['entity_name']
        score = details['score']
        parts = entity.split(".")

        # If entity is a column, add its score to its table's score
        if details['entity_type'] == "column":
            table_name = ".".join(parts[:2])
            db_name = parts[0]
            table_scores[table_name] = round(table_scores.get(table_name, 0) + score * f_column, 2)
            db_scores[db_name] = round(db_scores.get(db_name, 0) + score * f_column, 2)

        # If entity is a table, add its score with adjustment factor to both table and db score
        elif details['entity_type'] == "table":
            db_name = parts[0]
            table_scores[entity] = round(table_scores.get(entity, 0) + score * f_table, 2)
            db_scores[db_name] = round(db_scores.get(db_name, 0) + score * f_table, 2)

        # If entity is a db, add its score with adjustment factor
        elif details['entity_type'] == "db":
            db_scores[entity] = round(db_scores.get(entity, 0) + score * f_db, 2)

    # Sort tables by score and get the top N
    sorted_tables = sorted(table_scores.items(), key=lambda x: x[1], reverse=True)
    top_n_tables = sorted_tables[:top_n]

    # Filter out tables from dbs with scores lower than the threshold
    highest_db_score = max(db_scores.values())
    threshold = highest_db_score * db_score_threshold_ratio
    top_n_tables_filtered1 = [(t, s) for t, s in top_n_tables if db_scores[t.split(".")[0]] >= threshold]

    # Filter out tables with Table scores lower than the threshold
    top_n_tables_filtered2 = [(t, s) for t, s in top_n_tables_filtered1 if s >= table_score_threshold]

    # print tables by prettytable
    table = prettytable.PrettyTable(["编号", "表相关度", "库相关度", "表名", "状态"])
    table.align["表名"] = "l"
    table.align["状态"] = "l"

    i = 0
    table_results = []
    table_results += [(t, s, "⭐️") for t, s in top_n_tables_filtered2]
    table_results += [(t, s, f"❎（表的相关度低于阈值{table_score_threshold}）")
                      for t, s in set(top_n_tables_filtered1) - set(top_n_tables_filtered2)]
    table_results += [(t, s, f"❎（数据库的相关度低于阈值{highest_db_score}*{db_score_threshold_ratio}）")
                      for t, s in set(top_n_tables) - set(top_n_tables_filtered1)]
    table_results += [(t, s, f"❎ （表的相关度太低，不满足 TOP {top_n}）")
                      for t, s in set(sorted_tables) - set(top_n_tables)]

    # order by table score
    table_results = sorted(table_results, key=lambda x: x[1], reverse=True)
    for t, s, state in table_results:
        i += 1
        table.add_row([i, s, db_scores[t.split(".")[0]], t, state])
    log.info(f"\n{table}")
    return top_n_tables_filtered2


if __name__ == "__main__":
    pass