# -*- coding:utf-8 -*-

import unittest
from db.core import DbTemplate
import db.core
from db.factory import OracleConnectionFactory

CONNECT_URL = 'epayment/Epay789*QWE@localhost:15211/tyzf'
HOST = 'localhost'
USERNAME = 'epayment'
PASSWORD = 'Epay789*QWE'
PORT = 15211
SERVICE = 'tyzf'


class DBTest(unittest.TestCase):

    def setUp(self):
        connect_factory = OracleConnectionFactory(host=HOST, username=USERNAME,
                                                  password=PASSWORD, port=PORT, service=SERVICE)
        self.db_template = DbTemplate(connect_factory=connect_factory)

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

        results = self.db_template.query_list(sql, outputtypehandler=db.core.output_type_handler)
        if results is not None:
            for res in results:
                print res
        else:
            print "results is None"

if __name__ == '__main__':

    unittest.main()
