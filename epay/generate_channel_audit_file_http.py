# -*- coding:utf-8 -*-

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from util import db_utils
from database.core import makedict

SEPARATOR_TAB = '\t'
SEPARATOR_NEWLINE = '\n'

COMMON_AUDIT_FILE = [
    'channel_id',
    'rcv_user_id',
    'user_id',
    'user_type',
    'payment_order_id',
    'order_id',
    'cny_amount',
    'service_id',
    'order_time',
    'paid_time',
    'status',
    'company_code',
    'payment_method',
    'pay_org_trans_id',
    'city',
    'pay_trans_id'
]

CHINA_PAY_INSTALMENT_AUDIT_FIELD = [
    'preauth_amount',
    'interest_rate',
    'instalment_term',
    'interest_per_term',
    'interest_total']

# 对账方式
AUDIT_TYPE_CHANNEL = 0

AUDIT_TYPE_CHANNEL_SERVICE = 1

AUDIT_TYPE_CHANNEL_MARCHANT = 2

AUDIT_TYPE_INSTALMENT = 3


def query_order_by_order_time(channel_id, init_status, start_time, end_time):
    sql_builder = StringIO()
    sql_builder.write("select * from (")
    sql_builder.write("select po.channel_id, po.rcv_user_id, po.user_id, po.user_type, ")
    sql_builder.write("po.payment_order_id, po.order_id, po.amount,po.reversal_amount, po.points, po.service_id, ")
    sql_builder.write("po.order_time, po.paid_time, po.status, po.city, org.company_code, org.payment_method, ")
    sql_builder.write("po.cny_amount, po.instalment_term, po.interest_total, po.interest_rate, ")
    sql_builder.write("po.pay_org_id, po.paid_success_num, pl.pay_org_trans_id, pl.reverse_org_trans_id, pl.pay_trans_id,")
    sql_builder.write("rank () over (partition by pl.payment_order_id order by pl.pay_org_trans_id || pl.log_id) order_by_num ")
    sql_builder.write("from t_payment_order po, t_payment_log pl, t_payment_org org ")
    sql_builder.write("where po.payment_order_id = pl.payment_order_id and po.pay_org_id = org.org_id ")
    sql_builder.write("and po.channel_id = %s and po.status <> %s ")
    sql_builder.write("and po.order_time between %s and %s")
    sql_builder.write(") where order_by_num = 1")

    query_sql = sql_builder.getvalue()
    sql_builder.close()

    query_sql = query_sql % (channel_id, str(init_status), start_time, end_time)
    dbtmpl = db_utils.get_datatemplate()
    result = dbtmpl.query_list(query_sql, row_factory=makedict)
    return result


def write_audit_file(orders, file_path, start_time, end_time):
    with open(file_path, 'w') as f:
        f.write('%s\t%s\t%s\n' % (start_time, end_time, len(orders)))
        for idx in xrange(0, len(orders)):
            line = generate_audit_record(orders[idx])
            f.write(line)
            orders[idx] = None
            if idx % 1000 == 0:
                f.flush()


def generate_audit_record(order):
    audit_record_field = COMMON_AUDIT_FILE
    return '%s%s%s' % (SEPARATOR_TAB.join(['%s' % order[item] for item in audit_record_field]), SEPARATOR_TAB, SEPARATOR_NEWLINE)
if __name__ == '__main__':
    channel_id = '02'
    init_status = '0'
    start_time = '20170822000000'
    end_time = '20170823000000'
    orders = query_order_by_order_time(channel_id, init_status, start_time, end_time)
    write_audit_file(orders, file_path='%s-%s-%s' % (channel_id, start_time, end_time), start_time=start_time, end_time=end_time)