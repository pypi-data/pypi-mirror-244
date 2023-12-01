import unittest

from packages import transform_utils as tu

class TestTranslateSql(unittest.TestCase):

    def test_simple_snowflake_sql(self):
        sql = "SELECT * FROM XX-XX.YYY.my_table"
        input_ids = ['my_table']

        result = tu.translate_sql("snowflake-sql", sql=sql, input_ids=input_ids)

        expected_sql = "SELECT * FROM {{my_table}}"
        self.assertEqual(result, expected_sql)

    def test_simple_bigquery_sql(self):
        sql = "SELECT * FROM XX-XX.YYY.my_table"
        input_ids = ['my_table']

        result = tu.translate_sql("bigquery-sql", sql=sql, input_ids=input_ids)

        expected_sql = "SELECT * FROM {{my_table}}"
        self.assertEqual(result, expected_sql)

    def test_quoted_bigquery_sql(self):
        sql = "SELECT * FROM `XX-XX`.`YYY`.`my_table`"
        input_ids = ['my_table']

        result = tu.translate_sql("bigquery-sql", sql=sql, input_ids=input_ids)

        expected_sql = "SELECT * FROM {{my_table}}"
        self.assertEqual(result, expected_sql)
        
    def test_simple_databricks_sql(self):
        sql = "SELECT * FROM `XXX`.`YYY`.`my_table`"
        input_ids = ['my_table']

        result = tu.translate_sql("databricks-sql", sql=sql, input_ids=input_ids)

        expected_sql = "SELECT * FROM {{my_table}}"
        self.assertEqual(result, expected_sql)

    def test_wrong_databricks_sql(self):
        sql = "SELECT * FROM `XXX`.`YYY`.`ZZZ`"
        input_ids = ['my_table']

        result = tu.translate_sql("databricks-sql", sql=sql, input_ids=input_ids)

        self.assertEqual(result, sql)

    def test_wrong_bq_sql(self):
        sql = "SELECT * FROM XXX.YYY.ZZZ"
        input_ids = ['my_table']

        result = tu.translate_sql("bigquery-sql", sql=sql, input_ids=input_ids)

        self.assertEqual(result, sql)