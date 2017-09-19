# -*- coding: utf-8 -*-

import db_utils
from database.core import makedict

import sys
import os
import copy

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

reload(sys)
sys.setdefaultencoding('utf8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

SEPARATOR_TAB = '\t'
SEPARATOR_NEWLINE = '\n'

# 对账方式
AUDIT_TYPE_CHANNEL = 0

AUDIT_TYPE_CHANNEL_SERVICE = 1

AUDIT_TYPE_CHANNEL_MARCHANT = 2

AUDIT_TYPE_INSTALMENT = 3

# common audit record field
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


def query_audit_order_by_type(channel_id, merchant_id, settle_date, custom_type=None,city=None, service=None):
    condition_sql = StringIO.StringIO()
    prefix = """
    select * from (
        select 	
        po.channel_id, 
        po.rcv_user_id, 
        po.user_id, 
        po.user_type,
        po.payment_order_id, 
        po.order_id, 
        po.amount,
        po.reversal_amount, 
        po.points, 
        po.service_id, 
        po.order_time, 
        po.paid_time, 
        po.status, 
        org.company_code, 
        org.payment_method, 
        po.city, 
        po.cny_amount, 
        po.instalment_term, 
        po.interest_total, 
        po.interest_rate,
        pl.pay_trans_id,
        pl.settle_date, 
        pl.reversal_settle_date, 
        po.pay_org_id, 
        po.paid_success_num, 
        pl.pay_org_trans_id, 
        pl.reverse_org_trans_id, 
        rank () over (partition by pl.payment_order_id order by pl.settle_date || pl.reversal_settle_date || pl.log_id) order_by_num 
        from t_payment_order po, t_payment_log pl, t_payment_org org 
        where po.payment_order_id = pl.payment_order_id
        and po.pay_org_id = org.org_id
        and po.channel_id = '%s'"""

    if custom_type == AUDIT_TYPE_CHANNEL_SERVICE:
        condition_sql.write( " and po.service='%s' ")
    elif custom_type == AUDIT_TYPE_CHANNEL_MARCHANT:
        condition_sql.write( " and po.rcv_user_id='%s' ")
    elif custom_type == AUDIT_TYPE_INSTALMENT:
        condition_sql == condition_sql.write(" and po.city = %s")

    middle = condition_sql.getvalue()

    end =""" and (
        ((po.status = 2 or po.status = 3 or po.status = 6 or po.status = 7) and pl.bank_pay_status = 1 and pl.settle_date <= '%s' )
        or ((po.status = 3 or po.status = 6 or po.status = 7) and pl.bank_reverse_status = 1 and pl.reversal_settle_date <= '%s'))
    ) where order_by_num = 1 
    and (settle_date between '%s' and '%s' or reversal_settle_date between '%s' and '%s')"""

    sql = "%s%s%s" % (prefix, middle, end)

    audit_type = None
    if custom_type == AUDIT_TYPE_CHANNEL_SERVICE:
        audit_type = service
    elif custom_type == AUDIT_TYPE_INSTALMENT:
        audit_type = city
    elif custom_type ==AUDIT_TYPE_CHANNEL_MARCHANT:
        audit_type = merchant_id

    if audit_type is None:
        query_sql = sql % (channel_id, settle_date, settle_date, settle_date, settle_date, settle_date, settle_date)
    else:
        query_sql = sql % (channel_id, audit_type, settle_date, settle_date, settle_date, settle_date, settle_date, settle_date)
    # print query_sql
    dbtmpl = db_utils.get_datatemplate()

    result = dbtmpl.query_list(query_sql, row_factory=makedict)
    return result


def generate_audit_record(order, custom_type=None):
    audit_record_field = COMMON_AUDIT_FILE

    # generate audit by city
    if custom_type == AUDIT_TYPE_INSTALMENT:
        amount = int(order['amount'])
        pay_amount = int(order['cny_amount'])
        preauth_amount = amount - pay_amount
        interest_total = int(order['interest_total'])
        instalment_term = int(order['instalment_term'])
        interest_per_term = interest_total / instalment_term

        order['preauth_amount'] = '%s' % preauth_amount
        order['interest_per_term'] = '%s' % interest_per_term

        audit_record_field = audit_record_field + CHINA_PAY_INSTALMENT_AUDIT_FIELD

    return SEPARATOR_TAB.join(['%s' % order[item] for item in audit_record_field]) + SEPARATOR_TAB + SEPARATOR_NEWLINE


def write_audit_file(orders, file_path, settle_date, custom_type):
    start_time = settle_date + "000000"
    end_time = settle_date + "235959"
    with open(file_path, 'w') as f:
        f.write('%s\t%s\t%s\n' % (start_time, end_time, len(orders)))
        for idx in xrange(0, len(orders)):
            line = generate_audit_record(orders[idx], custom_type=custom_type)
            f.write(line)
            orders[idx] = None
            if idx % 1000 == 0:
                f.flush()


def generate_audit_file( merchant_id, channel_id, settle_date, custom_type, city=None, service=None):
    file_path = None
    if custom_type == AUDIT_TYPE_INSTALMENT:
        file_path = '%s_%s_%s_%s.txt' % (channel_id, merchant_id,city, settle_date)
    elif custom_type == AUDIT_TYPE_CHANNEL_SERVICE:
        file_path = '%s_%s_%s_%s.txt' % (channel_id, merchant_id, service, settle_date)
    else:
        file_path = '%s_%s_%s.txt' % (channel_id, merchant_id, settle_date)

    orders = query_audit_order_by_type(channel_id, merchant_id, settle_date, custom_type, city=city)

    if custom_type == AUDIT_TYPE_INSTALMENT:
        pay_order = []
        for order in orders:
            if order['status'] == 7 and order['channel_id'] == '32':
                new_order = copy.deepcopy(order)
                new_order['status'] = 2
                pay_order.append(new_order)
            if order['status'] == 3 and order['channel_id'] == '32' \
                    and settle_date == order['settle_date']:
                order['status'] = 2
        orders = orders + pay_order
    write_audit_file(orders, file_path, settle_date, custom_type)


if __name__ == '__main__':
    settle_date = '20170905'
    channel_id = '03'
    merchant = '010100GD001'

    generate_audit_file(merchant, channel_id, settle_date, AUDIT_TYPE_CHANNEL_MARCHANT)
