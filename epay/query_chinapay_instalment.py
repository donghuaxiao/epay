# -*- coding:utf-8 _-*-

import db_utils
import xlsxwriter

if __name__ == '__main__':
    sql = """
    SELECT ORDER_TIME,PAYMENT_ORDER_ID, ORDER_ID, CITY,STATUS
    FROM T_PAYMENT_ORDER 
    WHERE ORDER_TIME BETWEEN '20170701000000' AND '20170727235959'
    AND CHANNEL_ID = '32'"""

    header = [u'日期', u'支付单号', u'订单号', u'地市', u'支付状态']

    dbtmpl = db_utils.get_datatemplate()
    resp = dbtmpl.query_list(sql)

    wb = xlsxwriter.Workbook('ChinaPayInstalment.xlsx')
    sheet = wb.add_worksheet(u'银联分期')
    sheet
    sheet.write_row(0, 0, header)
    ind = 1
    for record in resp:
        sheet.write_row(ind, 0, record)
        ind += 1

    wb.close()