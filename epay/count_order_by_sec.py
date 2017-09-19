# -*_ coding:utf-8 -*-

#
#  按订单的时间统计订单数(所有), 根据 T_PAYMENT_ORDER 表的 order_time进行分组统计
#  如果统计的时间在两个月以前， 要对 T_PAYMENT_ORDER_HISTORY 表进行统计
#

from util import db_utils
from datetime import datetime, timedelta, date
import calendar
import os
import xlsxwriter

DIR='order_stat'
DATE_FROMAT = '%Y%m%d'


def date2str(day, format=DATE_FROMAT):
    if day is not None:
        return datetime.strftime(day, format)
    return None


def str2date(str_date, format=DATE_FROMAT):
    if str_date is None:
        return None
    try:
        return datetime.strptime(str_date, format)
    except ValueError as ex:
        print ex.message
        return None


def count_orders(day):
    start_time = day+'000000'
    end_time = day + '235959'
    sql = """
    select  order_time, count(*) from t_payment_order
    where order_time between :start_time and :end_time group by order_time
    """

    tmpl = db_utils.get_datatemplate()
    results = tmpl.query_list(sql, {'start_time': start_time, 'end_time': end_time})
    return results


def write_excel_file(day, results):
    wb = xlsxwriter.Workbook('%s%s%s.xlsx' % (DIR, os.sep, day))
    sheet = wb.add_worksheet('day')
    sheet.write_row(0, 0, [u'时间', u'订单数'])

    idx = 1
    for res in results:
        sheet.write_row(idx, 0, res)
        idx += 1
    wb.close()


def write_txt(day, results):
    with open('%s\%s.txt' % day, 'w') as f:
        for r in results:
            f.write('%s, %s\n' % r)


def max_count(results):
    if results is None or len(results) == 0:
        return 0
    counts = []
    for rs in results:
        counts.append(rs[1])
    return max(counts)


def get_month_range(year=None, month=None):
    """
    return the start date and the end date of specified month
    :param year:
    :param month:
    :return: (start_date, end_date)
    """
    if year is None:
        year = datetime.today().year
    if month is None:
        month = datetime.today().month
    start_date = date(year=year, month=month, day=1)
    _, days_in_month = calendar.monthrange(year, month)
    end_date = start_date + timedelta(days=days_in_month-1)
    return start_date, end_date


def _count_orders_by_date_range(start_date, end_date):

    while start_date <= end_date:
        day = date2str(start_date)
        results = count_orders(day)
        write_excel_file(day, results)
        print " day: %s max counts: %s" % (day, max_count(results))
        start_date += timedelta(days=1)


def count_orders_by_month(year=None, month=None):
    today = datetime.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month
    start_date, end_date = get_month_range(year, month)
    _count_orders_by_date_range(start_date, end_date)


def count_orders_by_date_range(year=None, month=None, start_date=None, end_date=None):
    today = datetime.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month
    startdate = date(year, month, start_date)
    enddate = date(year, month, end_date)
    _count_orders_by_date_range(startdate, enddate)


def count_orders_by_date_range(start_date, end_date):
    startdate = str2date(start_date)
    enddate = str2date(end_date)

    if startdate is None or enddate is None:
        print "date range  %s - %s for stat is not correct" % (start_date, end_date)
        return

    if start_date > end_date:
        print "start date %s is bigger than end date %s" % (start_date, end_date)
        return
    _count_orders_by_date_range(startdate, enddate)


def count_orders_by_date(day):
    count_date=None
    if isinstance(day, str):
        count_date = day
    elif isinstance(day, date):
        count_date = date2str(day)

    results = count_orders(count_date)
    write_excel_file(day, results)
    print " day: %s max counts: %s" % (day, max_count(results))


if __name__ == '__main__':

    """
        用法:
        #统计某一个时间之内的 每秒订单数
        count_orders_by_date_range( year=2017, month=7, start_date=1, end_date=8)
        
        # 统计某一个时间之内的 每秒订单数
        count_orders_by_date_range('20170801', '20170805')
        
        # 统计指定月的 每秒订单数
        count_order_by_month(year=2017, month=7)
        
        #统计指定某一天的 每秒订单数
        count_orders_by_date('20170805')
    """

    # print "start time : %s" % time_util.current_to_16()
    # count_orders_by_date(year=2017, month=7, start_date=1, end_date=2)
    # print "end time : %s" % time_util.current_to_16()

    #count_orders_by_date('20170803')
    #count_orders_by_date(date(2017, 8, 5))
    count_orders_by_date_range('20170820', '20170831')