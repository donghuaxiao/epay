# -*- coding:utf-8 -*-

import unittest
from database.core import DatabaeTemplate
import database.core
from database.factory import OracleConnectionFactory

CONNECT_URL = 'epayment/Epay789*QWE@localhost:15211/tyzf'
HOST = 'localhost'
USERNAME = 'epayment'
PASSWORD = 'Epay789*QWE'
PORT = 15215
SERVICE = 'tyzf'


class DBTest(unittest.TestCase):

    def setUp(self):
        connect_factory = OracleConnectionFactory(host=HOST, username=USERNAME,
                                                  password=PASSWORD, port=PORT, service=SERVICE)
        self.db_template = DatabaeTemplate(connect_factory=connect_factory)

    def test_connect(self):
        sql = 'SELECT count(*) as count from T_CITY'

        count = self.db_template.query_for_int(sql)
        print count

    def test_query_blob(self):
        sql = """
        SELECT ACCOUNT_ID as accountId, PARAM_CODE as code, PARAM_VALUE as value
        FROM T_PAYMENT_ACCOUNT_PARAM
        WHERE PARAM_CODE='PARENT_ACCOUNT_PID' AND ORG_ID LIKE 'Ali%' AND PARAM_VALUE IS NOT NULL
        """

        results = self.db_template.query_list(sql, outputtypehandler=database.core.output_type_handler,
                                              row_factory=database.core.makedict)
        if results is not None:
            for res in results:
                print res
        else:
            print "results is None"

    def test_desc(self):
        sql = "DESC T_PAYMENT_ORDER"

        self.db_template.execute(sql)

if __name__ == '__main__':

    unittest.main()
