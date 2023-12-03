# from langchain.chains import SimpleSequentialChain
# from cmysql.ai.mysql_database import QADatabaseChain, ExecSQLChain
# # from cmysql.ai.llm import InferMDataKGChain
# from cmysql.ai.graph_and_vector import FindMDataChain, ModifyMDataKGChain
#
#
# # generate_mdatakg_changes_chain = GenerateMDataKGChangesChain()
# modify_mdatakg_chain = ModifyMDataKGChain()
#
# # modify_mdatakg_from_feedback_chain = SimpleSequentialChain(
# #     ai=[generate_mdatakg_changes_chain, modify_mdatakg_chain],
# # )
#
# find_mdata_chain = FindMDataChain()  # 根据问题，找到相关的表
# qa_database_chain = QADatabaseChain()  # 查询数据，生成答案
#
# qa_chain = SimpleSequentialChain(
#     chains=[find_mdata_chain, qa_database_chain],
# )
#
# exec_sql_chain = ExecSQLChain()  # 执行SQL语句
#
#
# __all__ = [
#     "qa_chain",
#     "find_mdata_chain",
#     "qa_database_chain",
#     "modify_mdatakg_chain",
#     "exec_sql_chain",
# ]
#
#
# if __name__ == "__main__":
#     pass
#     # qa_chain.run("最近1个月，请假最多的人在哪个部门")
#     # modify_mdatakg_chain.run("表 mock_attendance 的字段 status 的含义再增加一种：0 表示未打卡")
#     # qa_chain.run("最近1星期，整个公司总共有多少次没打卡的情况")
#     # modify_mdatakg_from_feedback_chain.run("把t_product改成图书表")
#
#
#
