# -*- coding:utf-8 -*-

from database.factory import OracleConnectionFactory
from database.core import DatabaseTemplate
import database.core
from util.config import PropertiesParser
import time
import xlsxwriter
import os

import sys
reload(sys)
sys.setdefaultencoding('utf8')

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


def query_channel(dbtemplate):
    sql = "SELECT CHANNEL_ID, TITLE AS NAME FROM T_CHANNEL ORDER BY CHANNEL_ID"
    return dbtemplate.query_list(sql,
                                 row_factory=database.core.makedict)


def query_success_order_by_channel(dbtemplate, start_time, end_time):
    count_notify_success_sql = """
    SELECT CHANNEL_ID as channel_id,COUNT(*) as count FROM T_PAYMENT_ORDER			
    WHERE ORDER_TIME BETWEEN :start_time AND :end_time			
    AND status=2			
    GROUP BY CHANNEL_ID			
    ORDER BY CHANNEL_ID
    """
    params = {
        'start_time': start_time,
        'end_time': end_time,
    }
    return dbtemplate.query_list(count_notify_success_sql, params=params, row_factory=database.core.makedict)


def query_reversal_order(dbtemplate, start_time, end_time):
    count_orders_sql = """
    SELECT CHANNEL_ID as channel_id, COUNT(*) as count FROM T_PAYMENT_ORDER	
    WHERE ORDER_TIME BETWEEN :start_time AND :end_time	
    AND status=3
    GROUP BY CHANNEL_ID  	
    ORDER BY CHANNEL_ID	
    """

    params = {
        'start_time': start_time,
        'end_time': end_time
    }

    return dbtemplate.query_list(count_orders_sql, params=params, row_factory=database.core.makedict)


def query_message_count(dbtemplate, start_time, end_time):
    count_message_sql = """
    SELECT m.channel_id as channel_id, COUNT(*)	 as count	
    FROM t_message m, t_payment_order o			
    WHERE m.payment_order_id = o.payment_order_id			
    AND m.deliver_time BETWEEN :start_time AND :end_time			
    AND m.msg_type IN ('1','2')			
    AND m.status = 2			
    AND o.status = 2			
    GROUP BY m.channel_id			
    ORDER BY m.channel_id
    """
    params = {
        'start_time': start_time,
        'end_time': end_time
    }

    return dbtemplate.query_list(count_message_sql, params=params, row_factory=database.core.makedict)


def stat_channel_notify_rate(dbtemplate, start_time, end_time):
    begin_time = time.time()
    print "start time %s " % begin_time

    channels = query_channel(db_template)
    pay_orders = query_success_order_by_channel(dbtemplate, start_time, end_time)
    reversal_orders = query_reversal_order(dbtemplate, start_time, end_time)
    messages = query_message_count(dbtemplate, start_time, end_time)

    stat_datas = []
    header = [u'渠道ID', u'渠道名称'  u'总笔数', u'成功笔数', u'成功率']

    def get_count(datas, key):
        for data in datas:
            if data.get('channel_id') == key:
                return data.get('count')
        return 0

    for channel in channels:
        key = channel.get('channel_id')
        name = channel.get('name')

        order_count = get_count(pay_orders, key)
        reveral_count = get_count(reversal_orders, key) * 2
        message_count = get_count(messages, key)
        total = order_count + reveral_count

        if total == 0:
            notify_rate = 0
        else:
            notify_rate = (float(message_count) / total) * 100

        data = (key, name, total, message_count, notify_rate)
        stat_datas.append(data)

    wb = xlsxwriter.Workbook(u'通知成功率统计07.xlsx')
    sheet = wb.add_worksheet(u'7月成功率统计')
    cssformat = wb.add_format()
    cssformat.set_align('center')
    sheet.write_row(0, 0, header, cssformat)

    with open('result.txt', 'w') as f:
        try:
            for data in stat_datas:
                f.write("%s,%s,%s,%s,%s\n" % (data[0], data[1], data[2], data[3], data[4]))
        except Exception as ex:
            print ex.message

    ind = 1
    for row in stat_datas:
        sheet.write_row(ind, 0, row, cssformat)
        ind += 1
    wb.close()

    finish_time = time.time()
    print "end time %s" % finish_time
    print "use time: %s" % (finish_time - begin_time)

if __name__ == '__main__':
    props = PropertiesParser()
    props.read('epay.cfg')
    HOST = 'localhost'
    USERNAME = 'epayment'
    PASSWORD = 'Epay789*QWE'
    PORT = 15215
    SERVICE = 'tyzf'

    connect_factory = OracleConnectionFactory(host=HOST, username=USERNAME,
                                              password=PASSWORD, port=PORT, service=SERVICE)
    db_template = DatabaseTemplate(connect_factory=connect_factory)

    start_time = '20170701000000'
    end_time = '20170731235959'

    stat_channel_notify_rate(db_template, start_time, end_time)





