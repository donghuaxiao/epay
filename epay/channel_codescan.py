# -*- coding:utf-8 -*-

import re
import urllib2
import urllib
import random
import time

agreement = "http"
ip = "10.242.117.83"
port = 5000
svc_cat = 'PayTx'
svc_code = 'GetPaymentTDCURL'
alg = 'DESede'

request_url = 'http://localhost:8005/epay-test/index!bottom.action'

url_regex = re.compile(r'<p>webPaymentURL:(?P<url>http[s]?://.*?)</p>')

rand = random.Random()


def current_to_16():
    now = time.gmtime()
    return time.strftime('%Y%m%d%H%M%S', now)


def generate_order():
    prefix = current_to_16()
    return "%s%s" % (prefix, '000%s' %(rand.randint(0,10)))


def test_chinapay_tdc():
    order_time = current_to_16()
    order_id = generate_order()
    print "order_id :%s " % order_id
    req_data = {
        'agreement': agreement,
        'ip': ip,
        'port': port,
        'svc_cat': 'PayTx',
        'svc_code': 'GetPaymentTDCURL',
        'alg': 'DESede',
        'pwd': 'j90e8tzi7p3LQrq8KjnG9JjF',
        'channelID': '24',
        'serviceID': '30',
        'orderID': '%s' % order_id,
        'orderTime': '%s' % order_time,
        'merchant': '320100GD001',
        'user': '13800138000',
        'payUser': '13800138000',
        'point': 0,
        'amount': '1',
        'payMethod': 'ChinaPayInstalment',
        'title': '银联分期支付',
        'description': '银联分期支付',
        'orderURL': 'http://gd.10086.cn',
        'backURL': 'http://gd.10086.cn',
        'notifyURL': 'http://gd.10086.cn',
        'cashierDeskType': '0',
        'city': '020',
    }

    request = urllib2.Request(request_url)
    # request.get_method = lambda: 'POST'
    # resp = urllib2.urlopen(request, data=urllib.urlencode(req_data))
    request.add_data(urllib.urlencode(req_data))
    resp = urllib2.urlopen(request)
    if resp is None:
        print "resp is None"

    content = resp.read()
    matchs = url_regex.search(content)
    if matchs is None:
        return None
    return matchs.group('url')


if __name__ == '__main__':
    http_url = test_chinapay_tdc()
    print http_url
    if http_url != 'null' and http_url is not None:
        portal_url = http_url.replace('10.252.17.222:8080', 'gd.10086.cn')
        print portal_url

    else:
        print http_url