import os

AGENT_VERBOSE = True

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or input("请输入您的OpenAI API KEY: ")
OPENAI_PROXY = os.environ.get("OPENAI_PROXY", '')
OPENAI_LLM_VERBOSE = False
# OPENAI_LLM_MODEL_NAME = "gpt-3.5-turbo" # token太少，不推荐
OPENAI_LLM_MODEL_NAME = "gpt-4-1106-preview"
OPENAI_LLM_TEMPERATURE = 0
OPENAI_LLM_MAX_TOKENS = 4000
OPENAI_EMBEDDING_MODEL_NAME = "text-embedding-ada-002"
OPENAI_EMBEDDING_VECTOR_SIZE = 1536


class MySQLConfig:
    host = "localhost"
    port = 3306
    user = "root"
    password = ""
    db = "test"


class Neo4jConfig:
    uri = f"bolt://neo4j.datamini.ai:7687"
    user = "neo4j"
    password = "Pass1234"


class QdrantConfig:
    collection_name = "cmysql_collection"
    local_file_path = "/tmp/cmysql_vectors.db"  # 默认使用本地文件存储，如果local_file_path为空，则使用url连接server
    url = f"http://localhost:32769"



