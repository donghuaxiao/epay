# -*- coding: utf-8 -*-

from util import db_utils
from database.core import makedict
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def query_accounts_by_merchant(merchant_id):
    query_account = "select * from T_PAYMENT_ACCOUNT WHERE USER_ID = '%s'"
    print query_account % merchant_id
    dbtmpl = db_utils.get_datatemplate()
    accounts = dbtmpl.query_list(query_account % merchant_id, row_factory=makedict)
    return accounts


if __name__ == '__main__':
    merchant_id = '320100GD001'

    accounts = query_accounts_by_merchant(merchant_id)
    for account in accounts:
        print account['account_name']
