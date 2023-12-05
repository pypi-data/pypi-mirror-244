from cmysql.logs import log

from cmysql.ai.mysql_database import MySQLDatabase
from cmysql.ai.graph_and_vector import MDataKG
from cmysql.ai.generator import ai_generate
from cmysql.ai.prompts import INFER_MDATAKG_PROMPT


def init_brain(databases: list[str] = None) -> tuple:
    # extract meta data
    mdata = MySQLDatabase().retrieve_meta_data(databases=databases)

    # check if mdatakg exists
    kg = MDataKG()
    if kg.is_exist(mdata):
        log.info("最新抽取的 Meta Data 已存在，无需重复保存。")
        return 0, 0, 0, 0

    # infer and save mdatakg
    log.info(f"开始推测 MDataKG... 可能需要一点时间")
    mdatakg = ai_generate(
        INFER_MDATAKG_PROMPT,
        mdata=mdata,
    )
    db_count, table_count, column_count, c2c_relationship_count = kg.save(mdatakg)
    return db_count, table_count, column_count, c2c_relationship_count



