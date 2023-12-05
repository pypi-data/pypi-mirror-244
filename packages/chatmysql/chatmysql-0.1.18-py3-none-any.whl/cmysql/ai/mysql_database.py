import sqlalchemy as sa
from sqlalchemy import create_engine, text
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


if __name__ == "__main__":
    pass

