from os.path import dirname, join
import os
import unittest

from cmysql.tests.prompts import CHECK_SEMANTICS_PROMPT
from cmysql.tools import CHAT_LLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Must Import Config First
from cmysql.config import MySQLConfig as MC, Neo4jConfig as NC, QdrantConfig as QC
MC.db = "cmysql_unittest"
NC.uri = "neo4j://localhost:32796"
QC.collection_name = "cmysql_unittest"

from cmysql.ai.mysql_database import MySQLDatabase, QADatabaseChain, ExecSQLChain
from cmysql.ai.graph_and_vector import FindMDataChain, MDataKG
from cmysql.metabrain import init_brain
from cmysql.logs import log


def check_semantics(sentence1, sentence2):
    check_prompt = PromptTemplate(
        input_variables=["sentence1", "sentence2"],
        template=CHECK_SEMANTICS_PROMPT,
        template_format="jinja2"
    )
    check_chain = LLMChain(
        llm=CHAT_LLM,
        prompt=check_prompt,
    )
    check_result = check_chain.predict(
        sentence1=sentence1,
        sentence2=sentence2
    ).strip()

    if check_result == 'yes':
        log.info(f"『{sentence1}』和『{sentence2}』语义相同。")
        return True
    elif check_result == 'no':
        log.info(f"『{sentence1}』和『{sentence2}』语义不同。")
        return False
    else:
        raise Exception(f"check_semantics error: {check_result}")


class TestAll(unittest.TestCase):

    TEST_MYSQL_DB_SQL_FILE = join(
        dirname(__file__),
        "resources/database.sql"
    )
    TEST_TABLES = ["order_details", "orders", "products", "users"]

    mysql = MySQLDatabase()
    kg = MDataKG()

    @classmethod
    def setUpClass(cls):
        cls.mysql.engine.execute("create database if not exists " + MC.db)
        # exec sql file by mysql cli
        password_flag = f"-p{MC.password}" if MC.password else ""
        os.system(f"mysql -u {MC.user} {password_flag} -h {MC.host} -P {MC.port}"
                  f" {MC.db} < {cls.TEST_MYSQL_DB_SQL_FILE}")

        init_brain(databases=[MC.db])

    @classmethod
    def tearDownClass(cls):
        # clear mysql
        cls.mysql.engine.execute("drop database if exists " + MC.db)

        # clear mdatakg
        cls.kg.clear()

    def test_graph_connect(self):
        info = self.kg.graph_db.get_server_info()
        assert info.address.port == int(NC.uri.split(':')[-1]), info.address.port

    def test_retrieve_data(self):
        result = self.mysql.retrieve_data(f"show databases like '{MC.db}'")
        assert len(result) == 1

    def test_retrieve_meta_data(self):
        result = self.mysql.retrieve_meta_data()
        assert set(result["databases"][MC.db]["tables"].keys()) == set(self.TEST_TABLES)

    def _get_table_desc(self, table_full_name):
        table_desc = self.kg.get_desc_from_vector_db(table_full_name)
        return table_desc

    def test_modify(self):
        mdatakg_changes = {
            "desc": {
                f"{MC.db}.order_details": "订单详情",
            },
            "relationships": {
                "remove_c2c": [
                ],
                "add_c2c": [
                ],
                "modify_c2c": [
                ]
            }
        }
        self.kg.modify(mdatakg_changes)
        assert self._get_table_desc(f"{MC.db}.order_details") == "订单详情"

    def test_print_mdatakg(self):
        log.info(f"\n{self.kg}")

    def test_qa(self):
        question = "从10月1日到现在，总共卖了多少单？"
        mdata = self.kg.find(question=question)
        answer = self.mysql.qa(question, mdata)
        assert check_semantics(answer, "总共卖了2单")

    def test_infer_mdatakg_from_mdata(self):
        mdata = {
            'databases': {
                MC.db: {
                    'tables': {
                        'order_details': {
                            'desc': None,
                            'columns': {
                                'detail_id': None,
                                'order_id': None,
                                'product_id': None,
                                'quantity': None
                            }
                        },
                        'orders': {
                            'desc': None,
                            'columns': {
                                'order_id': None,
                                'user_id': None,
                                'total_price': None,
                                'created_at': None
                            }
                        }
                    }
                }
            }
        }
        mdatakg = self.kg.infer_mdatakg_from_mdata(mdata)
        assert "Entities" in mdatakg.keys()
        assert "Relationships" in mdatakg.keys()

    def test_modify_from_feedback(self):
        feedback = f'{MC.db}.order_details 是订单XYZ详细信息表'
        mdatakg_changes = self.kg.infer_mdatakg_changes_from_feedback(feedback)
        self.kg.modify(mdatakg_changes)
        assert self._get_table_desc(f"{MC.db}.order_details") == "订单XYZ详细信息表"

    def test_find_and_is_exist(self):
        mdata = self.kg.find("从10月1日到现在，总共卖了多少单？")
        assert "databases" in mdata.keys()
        assert self.kg.is_exist(mdata)


if __name__ == '__main__':
    unittest.main()
