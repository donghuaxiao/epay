# -*- coding:utf-8 -*-

import xlrd
import db_utils
import xlsxwriter

import database.core


def get_order_ids():
    wb = xlrd.open_workbook(filename='24_201706.xlsx')
    sheet = wb.sheet_by_name(u'梅州')

    nrows = sheet.nrows

    orders = []
    for row in xrange(1, nrows):
        row_data = sheet.row_values(row)
        if row_data[5] == '5':
            orders.append( row_data)
    order_ids = []
    for order in orders:
        order_ids.append(order[1])

    return "'" + "','".join(order_ids) + "'"

if __name__ == '__main__':
    ids = get_order_ids()
    dbtemplate = db_utils.get_datatemplate()

    sql = "SELECT PAYMENT_ORDER_ID,PAY_TRANS_ID, PAY_ORG_TRANS_ID, PAY_STATUS,PAY_LINK FROM T_PAYMENT_LOG WHERE PAYMENT_ORDER_ID IN ( %s )" % ids

    res = dbtemplate.query_list(sql)

    wb = xlsxwriter.Workbook('pay_failure.xlsx')
    sheet = wb.add_worksheet(u'支付失败订单')
    headers = [u'支付单号', u'支付流水号', u'支付宝交易流水', u'支付状态', u'链接']
    format = wb.add_format({'align': 'center'})

    sheet.write_row(0,0, headers, format)
    ind = 1
    for row in res:
        sheet.write_row(ind, 0, row, format)
        ind += 1

    wb.close()
