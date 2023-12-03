import uuid
import prettytable

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from qdrant_client import QdrantClient
from qdrant_client import models as qd_models
from qdrant_client.http.exceptions import ResponseHandlingException

from cmysql.logs import log
from cmysql.tools import calculate_top_related_tables
from cmysql.config import OPENAI_EMBEDDING_VECTOR_SIZE
from cmysql.config import Neo4jConfig as NC
from cmysql.config import QdrantConfig as QC
from cmysql.exceptions import MDataKGInitError
from cmysql.ai.openai_client import openai_llm

class MDataKG(object):
    graph_db = GraphDatabase.driver(uri=NC.uri, auth=(NC.user, NC.password))
    if QC.local_file_path:
        vector_db = QdrantClient(path=QC.local_file_path)
    else:
        vector_db = QdrantClient(url=QC.url)
    vector_db_collection = QC.collection_name
    precision_rate_threshold = 0.6

    def __init__(self):
        # test graph db is connected
        with self.graph_db.session() as session:
            try:
                session.run("MATCH (n) RETURN n LIMIT 1")
            except ServiceUnavailable as e:
                raise MDataKGInitError("图数据库连接失败，请检查图数据库的连接信息。")

        # test vector db is connected
        try:
            self.vector_db.get_collections()
        except ResponseHandlingException as e:
            raise MDataKGInitError("向量数据库连接失败，请检查向量数据库的连接信息。")

    def _save_graph_data(self, mdatakg: dict) -> tuple:
        # Initializing counters
        db_count = 0
        table_count = 0
        column_count = 0
        c2c_relationship_count = 0

        with self.graph_db.session() as session:
            # Delete all nodes and relationships
            # session.run("MATCH (n) DETACH DELETE n")

            # Create Database nodes
            for database_name, database_value in mdatakg["Entities"]["databases"].items():
                session.run("MERGE (D:Database {desc: $desc, name: $name})",
                            name=database_name, desc=database_value["desc"])
                db_count += 1

                # Create Table nodes inside each Database
                for table_name, table_value in database_value["tables"].items():
                    session.run("MERGE (T:Table {desc: $desc, name: $name, short_name: $short_name})",
                                name=f"{database_name}.{table_name}", short_name=table_name,
                                desc=table_value["desc"])
                    table_count += 1

                    session.run("""
                        MATCH (D:Database {name: $database_name}), (T:Table {name: $table_full_name})
                        MERGE (T)-[:T2D]->(D)
                    """, database_name=database_name, table_full_name=f"{database_name}.{table_name}")

                    # Create Column nodes inside each Table
                    for col_name, col_desc in table_value["columns"].items():
                        # col_name = column.split(":")[0].strip()
                        # col_desc = column.split(":")[1].strip()
                        full_col_name = f"{database_name}.{table_name}.{col_name}"
                        session.run("MERGE (C:Column {desc: $desc, name: $name, short_name: $short_name})",
                                    name=full_col_name, short_name=col_name, desc=col_desc)
                        column_count += 1

                        session.run("""
                            MATCH (T:Table {name: $table_full_name}), (C:Column {name: $full_col_name})
                            MERGE (C)-[:C2T]->(T)
                        """, table_full_name=f"{database_name}.{table_name}", full_col_name=full_col_name)

                # Create COLUMN_TO_COLUMN relationships
                for relationship in mdatakg["Relationships"]["column_to_column"]:
                    if relationship["precision_rate"] >= self.precision_rate_threshold:
                        session.run("""
                            MATCH (C1:Column {name: $from_node}), (C2:Column {name: $to_node})
                            MERGE (C1)-[:C2C {precision_rate: $precision_rate}]->(C2)
                        """,
                                    from_node=relationship["from"],
                                    to_node=relationship["to"],
                                    precision_rate=relationship["precision_rate"])
                        c2c_relationship_count += 1
        log.debug(f"插入了 {db_count} 个数据库，{table_count} 个表，{column_count} 个字段，{c2c_relationship_count} 个关联关系。")
        return db_count, table_count, column_count, c2c_relationship_count

    def __str__(self) -> str:
        # Fetching data from the graph
        with self.graph_db.session() as session:
            result = session.run("""
                MATCH (D:Database)-[:T2D]-(T:Table)
                RETURN D.name AS db_name, D.desc AS db_desc, T.short_name AS table_name, T.desc AS table_desc
                ORDER BY db_name, table_name
            """)

            # Organizing the data hierarchically
            data_hierarchy = {}
            for record in result:
                db_name = record["db_name"]
                if db_name not in data_hierarchy:
                    data_hierarchy[db_name] = {
                        "desc": record["db_desc"],
                        "tables": []
                    }

                table_data = (record["table_name"], record["table_desc"])
                data_hierarchy[db_name]["tables"].append(table_data)

        content_str = ""
        # For each database, print its details and its tables in separate tables
        for db_name, db_data in data_hierarchy.items():
            # Print the tables for this database
            table_table = prettytable.PrettyTable()
            table_table.title = f"DB: {db_name}"
            table_table.field_names = ["表", "描述"]
            table_table.align["描述"] = "l"
            table_table.align["表"] = "l"
            for table_name, table_desc in db_data["tables"]:
                table_table.add_row([table_name, table_desc])
            content_str += f"\n{table_table}\n"
        return content_str

    def _create_vector_collection(self):
        try:
            self.vector_db.get_collection(collection_name=self.vector_db_collection)
            return
        except:
            pass

        # 重建或创建新的集合
        self.vector_db.recreate_collection(
            collection_name=self.vector_db_collection,
            vectors_config=qd_models.VectorParams(size=OPENAI_EMBEDDING_VECTOR_SIZE,
                                                  distance=qd_models.Distance.COSINE),
        )

        # # 对name创建索引
        # self.vector_db.create_payload_index(
        #     collection_name=self.vector_db_collection,
        #     field_name="name",
        #     field_schema="keyword",
        # )

    def _save_vector_data(self, mdatakg: dict) -> int:
        self._create_vector_collection()

        # 准备要插入的数据点
        points = []

        entities = []
        for db_name, db_value in mdatakg["Entities"]["databases"].items():
            entities.append(("db", db_name, db_value["desc"]))

            for table_name, table_value in db_value["tables"].items():
                entities.append(("table", ".".join([db_name, table_name]), table_value["desc"]))

                for col_name, col_desc in table_value["columns"].items():
                    # col_name = column.split(":")[0].strip()
                    # col_desc = column.split(":")[1].strip()
                    entities.append(("column",  ".".join([db_name, table_name, col_name]), col_desc))

        # 按照批处理生成嵌入
        _BATCH_SIZE = 100
        for i in range(0, len(entities), _BATCH_SIZE):
            batch_texts = [entity[2] for entity in entities[i:i + _BATCH_SIZE]]
            # _embeddings = EMBEDDING_MODEL.embed_documents(batch_texts)
            _embeddings = openai_llm.embedding_batch(batch_texts)
            for j, (entity_type, entity_name, entity_desc) in enumerate(entities[i:i + _BATCH_SIZE]):
                points.append(
                    qd_models.PointStruct(
                        id=str(uuid.uuid1()),
                        vector=_embeddings[j],
                        payload={"type": entity_type, "name": entity_name, "desc": entity_desc}
                    )
                )

        # 插入数据点
        self.vector_db.upsert(collection_name=self.vector_db_collection, points=points)
        log.debug(f"插入了 {len(points)} 个向量。")
        return len(points)

    def save(self, mdatakg: dict) -> tuple:
        self._save_vector_data(mdatakg)
        counts = self._save_graph_data(mdatakg)
        return counts

    def _clear_vector_data(self):
        self.vector_db.delete_collection(self.vector_db_collection)
        log.info("向量数据已删除")

    def _clear_graph_data(self):
        with self.graph_db.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        log.info("图数据已删除")

    def clear(self):
        self._clear_graph_data()
        self._clear_vector_data()

    def modify(self, mdatakg_changes: dict) -> tuple:
        node_count = 0
        c2c_remove_count = 0
        c2c_add_count = 0
        c2c_modify_count = 0

        with self.graph_db.session() as session:
            if "desc" in mdatakg_changes:
                for node_name, new_desc in mdatakg_changes["desc"].items():
                    # update node desc in graph db
                    session.run("MATCH (n {name: $node_name}) SET n.desc = $new_desc", node_name=node_name,
                                new_desc=new_desc)

                    # replace node desc in vector db, delete and insert
                    # delete vector
                    self.vector_db.delete(
                        collection_name=self.vector_db_collection,
                        points_selector=qd_models.Filter(
                            must=[
                                qd_models.FieldCondition(
                                    key="name",
                                    match=qd_models.MatchValue(value=node_name),
                                )
                            ]
                        )
                    )

                    # insert vector
                    node_type = "unknown'"
                    if len(node_name.split('.')) == 1:
                        node_type = "db"
                    elif len(node_name.split('.')) == 2:
                        node_type = "table"
                    elif len(node_name.split('.')) == 3:
                        node_type = "column"

                    self.vector_db.upsert(
                        collection_name=self.vector_db_collection,
                        points=[
                            qd_models.PointStruct(
                                id=str(uuid.uuid1()),
                                payload={
                                    "name": node_name,
                                    "type": node_type,
                                    "desc": new_desc
                                },
                                # vector=EMBEDDING_MODEL.embed_documents([new_desc])[0],
                                vector=openai_llm.embedding(new_desc)
                            ),
                        ]
                    )

                    node_count += 1

            if "relationships" in mdatakg_changes:
                relationship_changes = mdatakg_changes["relationships"]
                if "remove_c2c" in relationship_changes:
                    for change in relationship_changes["remove_c2c"]:
                        from_column, to_column = change.split(" -> ")
                        session.run("""
                            MATCH (C1:Column {name: $from_column})-[r:C2C]->(C2:Column {name: $to_column})
                            DELETE r
                        """, from_column=from_column, to_column=to_column)
                        c2c_remove_count += 1

                if "add_c2c" in relationship_changes:
                    for change in relationship_changes["add_c2c"]:
                        from_column, to_column = change.split(" -> ")
                        session.run("""
                            MATCH (C1:Column {name: $from_column}), (C2:Column {name: $to_column})
                            MERGE (C1)-[:C2C {precision_rate: 0.8}]->(C2)
                        """, from_column=from_column, to_column=to_column)
                        c2c_add_count += 1

                if "modify_c2c" in relationship_changes:
                    for change in relationship_changes["modify_c2c"]:
                        from_column, to_column_and_precision = change.split(" -> ")
                        to_column, precision_rate = to_column_and_precision.split(" : ")
                        session.run("""
                            MATCH (C1:Column {name: $from_column})-[r:C2C]->(C2:Column {name: $to_column})
                            SET r.precision_rate = $precision_rate
                        """, from_column=from_column, to_column=to_column, precision_rate=float(precision_rate))
                        c2c_modify_count += 1
        result = (f"更新节点备注：{node_count}个, 删除字段关系：{c2c_remove_count}个, "
                   f"新增字段关系：{c2c_add_count}个, 更新字段关系的概率：{c2c_modify_count}个。")
        return node_count, c2c_remove_count, c2c_add_count, c2c_modify_count, result

    def find(self, question: str,
             databases: list[str] = None,
             search_limit: int = 100,
             top_n: int = 10,
             table_score_threshold: float = 4.0
            ) -> dict:
        # Step 1: Use the vector database to get the most related entities based on the question
        # question_embedding = EMBEDDING_MODEL.embed_documents([question])[0]
        question_embedding = openai_llm.embedding(question)

        # Search the vector database
        results = self.vector_db.search(
            collection_name=self.vector_db_collection,
            query_vector=question_embedding,
            limit=search_limit
        )
        similar_search_results = [{"name": result.payload["name"],
                                   "type": result.payload["type"],
                                   "score": result.score}
                                  for result in results]
        top_n_tables = calculate_top_related_tables(similar_search_results,
                                                    top_n=top_n,
                                                    table_score_threshold=table_score_threshold
                                                    )
        if not top_n_tables:
            return {}

        # Step 2: Use the graph database to get related tables and columns
        mdata = {"databases": {}}
        with self.graph_db.session() as session:
            for full_table_name, _ in top_n_tables:
                columns = session.run("""
                        MATCH (T:Table {name: $full_table_name})<-[:C2T]-(C:Column)
                        RETURN C.name, C.desc
                    """, full_table_name=full_table_name)

                columns_dict = {}
                for col in columns:
                    # columns_list.append(f"{col['C.name'].split('.')[-1]}: {col['C.desc']}")
                    columns_dict[col['C.name'].split('.')[-1]] = col['C.desc']

                table_comment = session.run("""
                        MATCH (T:Table {name: $full_table_name})
                        RETURN T.desc
                    """, full_table_name=full_table_name).single().get('T.desc')

                short_table_name = full_table_name.split('.')[-1]
                db_name = full_table_name.split('.')[0]
                if db_name not in mdata["databases"]:
                    db_desc = session.run("""
                            MATCH (D:Database {name: $db_name})
                            RETURN D.desc
                        """, db_name=db_name).single().get('D.desc')
                    mdata["databases"][db_name] = {"desc": db_desc, "tables": {}}

                mdata["databases"][db_name]["tables"][short_table_name] = {"desc": table_comment,
                                                                           "columns": columns_dict}
        # 使用 prettytable 打印 top_n_tables 为表格，方便阅读，两列，第一列为相关度，第二列为表名，按得分降序排列，内容左对齐
        table = prettytable.PrettyTable(["相关度", "表名"])
        table.align["相关度"] = "l"
        table.align["表名"] = "l"
        for table_name, score in top_n_tables:
            table.add_row([score, table_name])
        log.info(f"根据您的问题 『{question}』， 找到{len(top_n_tables)}个表：\n{table}。")

        return mdata

    def is_exist(self, mdata: dict) -> bool:
        with self.graph_db.session() as session:
            # 1. Check each database in MData
            for db_name, db_content in mdata["databases"].items():
                db_result = session.run("""MATCH (D:Database {name: $db_name}) RETURN D.name""",
                                        db_name=db_name)
                if not db_result.single():
                    return False

                # 2. Check each table in the database
                for table_name, table_info in db_content["tables"].items():
                    table_result = session.run("""MATCH (T:Table {name: $table_full_name}) RETURN T.name""",
                                               table_full_name=f"{db_name}.{table_name}")
                    if not table_result.single():
                        return False

                    # 3. Check each column in the table
                    for column_name, column_desc in table_info["columns"].items():
                        # column_name = column.split(":")[0].strip()
                        full_col_name = f"{db_name}.{table_name}.{column_name}"
                        col_result = session.run("""MATCH (C:Column {name: $full_col_name}) RETURN C.name""",
                                                 full_col_name=full_col_name)
                        if not col_result.single():
                            return False

        return True

    def get_desc_from_vector_db(self, obj_name):
        result = self.vector_db.scroll(
            collection_name=self.vector_db_collection,
            scroll_filter=qd_models.Filter(
                must=[
                    qd_models.FieldCondition(
                        key="name",
                        match=qd_models.MatchValue(value=obj_name),
                    )
                ]
            ),
            limit=1,
        )
        if not result:
            log.error(f"向量数据库中没有找到 {obj_name} 。")
            return None
        # log.info(f"向量数据库中找到了 {obj_name} , 结果：{result}。")
        return result[0][0].payload["desc"]


if __name__ == "__main__":
    pass
