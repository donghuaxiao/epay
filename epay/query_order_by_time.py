# -*- coding:utf-8 -*-

import xlsxwriter

from util import db_utils


def query_order( order_time ):
    sql = "select order_time, payment_order_id, channel_id, status from t_payment_order where order_time = '%s'"

    tmpl = db_utils.get_datatemplate()

    results = tmpl.query_list(sql % order_time)
    return results


def write_excel(orders):
    wb = xlsxwriter.Workbook("orders.xlsx")

    sheet = wb.add_worksheet('orders')

    title = [u'订单时间', u'订单号', u'渠道', u'状态']

    sheet.write_row(0, 0, title)

    idx = 1

    for order in orders:
        sheet.write_row(idx, 0, order)
        idx += 1
    wb.close()


if __name__ == '__main__':
    order_time = '20170812003421'
    orders = query_order(order_time)
    write_excel(orders)