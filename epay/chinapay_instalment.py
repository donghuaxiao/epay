# -*- coding:utf-8 -*-

from util import time_util
import re
import urllib2
import urllib

agreement = "http"
ip = "10.242.117.83"
port = 5005
svc_cat = 'PayTx'
svc_code = 'GetPaymentTDCURL'
alg = 'DESede'

request_url = 'http://localhost:8005/epay-test/index!bottom.action'

url_regex = re.compile(r'<p>webPaymentURL:(?P<url>http[s]?://.*?)</p>')


def chinapay_tdc():
    order_time = time_util.current_to_16()
    order_id = time_util.generate_order()
    print "order_id :%s " % order_id
    req_data = {
        'agreement': 'http',
        'ip': '10.252.42.107',
        'port': '5000',
        'svc_cat': 'PayTx',
        'svc_code': 'GetPaymentTDCURL',
        'alg': 'DESede',
        'pwd': 'j90e8tzi7p3LQrq8KjnG9JjF',
        'channelID': '32',
        'serviceID': '30',
        'orderID': '%s' % order_id,
        'orderTime': '%s' % order_time,
        'merchant': '320100GD001',
        'user': '13800138000',
        'payUser': '13800138000',
        'point': 0,
        'amount': '12',
        'payMethod': 'ChinaPayInstalment',
        'title': '银联分期支付',
        'description': '银联分期支付',
        'orderURL': 'http://gd.10086.cn',
        'backURL': 'http://gd.10086.cn',
        'notifyURL': 'http://gd.10086.cn',
        'cashierDeskType': '0',
        'city': '020',
        'tradeAmount': 0,
        'marketingCode': 'test_code',
        'marketingName': '测试类别',
        'intrestType': 0  # 有利息
    }

    request = urllib2.Request(request_url)
    # request.get_method = lambda: 'POST'
    # resp = urllib2.urlopen(request, data=urllib.urlencode(req_data))
    request.add_data(urllib.urlencode(req_data))
    resp = urllib2.urlopen(request)
    if resp is None:
        print "resp is None"

    content = resp.read()
    #print content
    matchs = url_regex.search(content)
    if matchs is None:
        return None
    return matchs.group('url')


if __name__ == '__main__':
    http_url = chinapay_tdc()
    print http_url
    if http_url != 'null' and http_url is not None:
        portal_url = http_url.replace('10.252.17.222:8080', 'gd.10086.cn')
        print portal_url

    else:
        print http_url