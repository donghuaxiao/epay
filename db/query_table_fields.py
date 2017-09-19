# -*- coding:utf-8 -*-

from util import db_utils

SEP = '，'
def query_table_fields(table_name):
    sql = """
    select utc.column_name 
    from USER_TAB_COLUMNS utc, user_tables ut
    where utc.table_name = ut.table_name and ut.table_name=:table_name
    """

    tmpl = db_utils.get_datatemplate()
    res = tmpl.query_list(sql, {'table_name': table_name})
    fields = [re[0] for re in res]
    return fields


if __name__ == '__main__':
    fields = query_table_fields('T_PAYMENT_USER')
    print SEP.join(fields)