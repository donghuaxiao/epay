# -*- coding:utf-8 -*-

import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from util import ssh_util

username='user'
password='tyzF123!@#'
ip = 'localhost'
port = 9822

str_time = """
2017-09-08 17:43:14,895 DEBUG [com.ericsson.epay.dispatch.endpoint.jetty.JettyContext] [qtp1747715424-18314] [JettyContext.java:58] - <Output:<?xml version="1.0" encoding="UTF-8" standalone="yes"?><CreatePaymentOrderResp xmlns="http://www.chinamobile.com/paymentportal"><Result>0</Result><PaymentOrderID>252017090817431402318064</PaymentOrderID><ChannelName>肇庆移动和商汇</ChannelName><ServiceName>充值缴费</ServiceName><Description>返回创建支付单响应成功信息</Description><PayService><PayServiceID>AliPayWAP</PayServiceID><PayServiceName>支付宝</PayServiceName><PayOrgCode>91</PayOrgCode><PayOrgName>支付宝</PayOrgName><PayInterfaceType>1</PayInterfaceType><PayInterfaceName>网银</PayInterfaceName><UserAuthenFlag>1</UserAuthenFlag><PayMethod>13</PayMethod><PayMethodName>支付宝支付</PayMethodName><Status>1</Status><DisplayBankFlag>0</DisplayBankFlag><PayDirect>1</PayDirect><UsingGuide>支持储蓄卡、信用卡及支付宝</UsingGuide><UsingFrequency>0</UsingFrequency><PayChannelType>0</PayChannelType><PayOrgType>2</PayOrgType></PayService><CashierDeskType>0</CashierDeskType><Reminder>亲，以上订单信息请您确认哦！</Reminder><RepayFlag>0</RepayFlag><TimeOut>30</TimeOut></CreatePaymentOrderResp>>
"""

str_test = 'sfesf<OrderID>aaabbbbcc</OrderID>'

regex = re.compile(r'(?P<time>\d+-\d+-\d+ \d+:\d+:\d+,\d+) .*<OrderID>(?P<orderId>.*)</OrderID><OrderTime>(?P<orderTime>.*)</OrderTime>')
regex2 = re.compile(r'(?P<time>\d+-\d+-\d+ \d+:\d+:\d+,\d+) .*<PaymentOrderID>(?P<pid>.*)</PaymentOrderID>')

reg = re.compile(r'<OrderID>(?P<orderId>.*)</OrderID>')

def grep():
    order_time = []
    cmd = 'grep  --color=never 23010758001 /usr/local/epay/epay-platform/logs/dispatch.log | grep --color=never CreatePaymentOrderReq'
    ssh_client = ssh_util.SSHConnection(host=ip, username=username, password=password, port=port)
    outputs = ssh_client.exec_command(cmd)
    for line in outputs:
        order_time.append(fetch_item(line))

    with open('req2.txt', 'w') as f:
        for order in order_time:
            f.write('%s\t%s\t%s\n' % (order))


def fetch_item(line):
    mg = re.search(regex, line)
    return mg.group('orderId'), mg.group('time'),  mg.group('orderTime')


def grep_response(payment_order_id):
    cmd = 'grep --color=never %s /usr/local/epay/epay-platform/logs/dispatch.log | grep CreatePaymentOrderResp'
    ssh_client = ssh_util.SSHConnection(host=ip, username=username, password=password, port=port)
    outputs = ssh_client.exec_command(cmd % payment_order_id)
    for line in outputs:
        print line


if __name__ == '__main__':

    grep()
    # with open('payment_order.txt', 'r') as f:
    #     for line in f:
    #         grep_response(line)
