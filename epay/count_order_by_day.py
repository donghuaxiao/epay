# -*- coding:utf-8 -*-

# Count order by day

from datetime import datetime, timedelta
from util import db_utils
import xlsxwriter

try:
    from cStringIO import StringIO as StringIO
except ImportError:
    from StringIO import StringIO

count_sql = 'SELECT COUNT(*) FROM T_PAYMENT_ORDER WHERE ORDER_TIME BETWEEN :start_time AND :end_time'
count_sql_by_channel = 'SELECT CHANNEL,COUNT(*)'
DATE_FORMAT = '%Y%m%d'


def str2day(str_day, format=DATE_FORMAT):
    try:
        return datetime.strptime(str_day, format)
    except ValueError as e:
        print e.message
        return None


def day2str(day, format=DATE_FORMAT):
    try:
        return datetime.strftime(day, format)
    except ValueError as e:
        print e.message
        return None


def count_order_by_date_range(start_day, end_day):
    start_date = str2day(start_day)
    end_date = str2day(end_day)

    if start_date is None:
        print "start_day: %s is not correct" % start_day
        return
    if end_day is None:
        print "end_day: %s is not correct" % end_day
        return
    if start_date > end_date:
        print "start_day is bigger than end_date"
        return
    results = {}
    while start_date <= end_date:
        count = count_order_by_day(start_date)
        print '%s: %s' % (day2str(start_date), count)
        results[day2str(start_date)] = count
        start_date += timedelta(days=1)
    return results


def count_order_by_day(day):
    start_time = day2str(day) + '000000'
    end_time = day2str(day) + '235959'
    tmpl = db_utils.get_datatemplate()
    params = {
        'start_time': start_time,
        'end_time': end_time
    }
    count = tmpl.query_for_int(count_sql, params)
    return count


def write_excel(file_name, sheet_name=None, header=None, results=None):
    wb = xlsxwriter.Workbook(file_name)
    sheet = wb.add_worksheet(sheet_name)
    sheet.write_row(0, 0, header)
    idx = 1
    for result in results:
        sheet.write_row(idx, 0, result)
        idx += 1
    wb.close()


def count_order_by_status(start_time, end_time, channel_id=None):
    params = {
        'start_time': start_time,
        'end_time': end_time
    }

    count_sql = StringIO()
    count_sql.write("SELECT CHANNEL_ID, count(*) as total, SUM(case when STATUS = 2 then  1 else 0 end) as success_num,")
    count_sql.write("SUM(case when STATUS = 3 or STATUS = 6 or STATUS=7 then 1 else 0 end )as refund_num,")
    count_sql.write("SUM(case when status=4 or status = 5 then 1 else 0 end) as failure_num ")
    count_sql.write("FROM T_PAYMENT_ORDER WHERE ORDER_TIME BETWEEN :start_time AND :end_time ")
    if channel_id is not None:
        count_sql.write(" AND CHANNEL_ID = :channel_id ")
        params['channel_id'] = channel_id

    count_sql.write(" GROUP BY CHANNEL_ID ORDER BY CHANNEL_ID")
    query_sql = count_sql.getvalue()
    count_sql.close()

    tmpl = db_utils.get_datatemplate()

    try:
        return tmpl.query_list(query_sql, params)
    except Exception as ex:
        print ex.message
        return None


if __name__ == '__main__':
    # results = count_order_by_date_range('20170801', '20170831')
    # sorted_key = sorted(results.keys())
    # values = [(key, results[key]) for key in sorted_key]
    # headers = [u'日期', u'订单数']
    # file_name = u'8月订单量统计.xlsx'
    # sheet_name=u'月订单量统计'
    # write_excel(file_name, sheet_name=sheet_name, header=headers, results=values)

    headers = [u'渠道ID', u'总订单数', u'支付成功数', u'退款数', u'支付失败数']
    #order_count = count_order_by_status('20170908000000', '20170908235959', channel_id=25)
    #write_excel(u'8月订单支付情况统计.xlsx', u'8月订单支付率统计', header=headers, results=order_count)

    print count_order_by_day(datetime.now())