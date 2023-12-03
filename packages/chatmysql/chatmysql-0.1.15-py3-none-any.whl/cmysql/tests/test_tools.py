from cmysql.tools import calculate_top_related_tables
import unittest


class TestTools(unittest.TestCase):

    def test_calculate_top_related_tables(self):
        similar_search_results1 = [
            {"type": "column", "name": "db1.table1.col1", "score": 0.3},
            {"type": "table", "name": "db1.table1", "score": 0.8},
            {"type": "column", "name": "db2.table2.col2", "score": 0.8},
            {"type": "column", "name": "db2.table2.col3", "score": 0.9},
            {"type": "table", "name": "db3.table2", "score": 0.3},
            # ... Add more results as needed
        ]
        top_related_tables = calculate_top_related_tables(similar_search_results1,
                                                          table_score_threshold=0.1)
        assert top_related_tables[0] == ('db2.table2', 1.7)
        assert top_related_tables[1] == ('db1.table1', 1.5)


if __name__ == '__main__':
    unittest.main()
