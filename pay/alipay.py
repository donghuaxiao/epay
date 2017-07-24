# -*- coding:utf-8 -*-

from pay.certsupport import alipaysupport

# from urllib2 import urlopen
import requests
import base64
import xml.dom.minidom
from xml.dom.minidom import parseString


def query_order(partern, order_id, private_key):
    """
    query the specified order's status
    :param partner: alipay partner
    :param order_id:  the order want to query
    :param private_key: private key
    :return: None
    """
    request_data = {
        'partner': partern,
        'service': 'single_trade_query',
        '_input_charset': 'UTF-8',
        'out_trade_no': order_id
    }

    sign = alipaysupport.sign_data(private_key, request_data)

    request_data.update({'sign': sign, 'sign_type': 'RSA'})
    print request_data

    api_url = 'https://mapi.alipay.com/gateway.do'
    res = requests.get(api_url, params=request_data)
    return res.text

def get_node_text(node):
    if node is None:
        return None
    for text_node in node.childNodes:
        if text_node.nodeType == text_node.TEXT_NODE:
            return text_node.data

def parse_query_result(result):
    if result is None:
        return None
    result = result.encode('utf-8')
    result_dom = parseString(result)
    is_success = result_dom.getElementsByTagName('is_success')[0]

    print "is_success : %s, error:%s" % (get_node_text(is_success), get_node_text(error))

if __name__ == '__main__':
    out_trade_no = '201707170855170400131945'
    partern = '2088421589772560'
    private_key = 'MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAMC2VH+ZYLKZqePIZUsf3Gc7ku5PgLC2Kk4y0ywivQUPgmiLKwDjr2AQ29mBkZXPm0Wo6frNdVLKJr/7eghF2Za+E85GsM+nKUOGDfBN34DhThlZtT5L09I9PHBVOcjQCDhY8cuthfmuHNqoV35QGfY5iU+xLmOnoMMV9uuGFIaHAgMBAAECgYAT3DaFF+dxQIjTorldrqDmOqt/x825aGyftnkw2Tulo92KrJz38H8IZXRizAmW6NhVq3zBjh8DMzYfHumKpLgxtPdq04Gi9T2eN6pE3k3d4qLUhYAklxLsPOZ4LU4yBwjmfqwDlTTKew0axkBfD+AiLMymRgbrbsM8mcQZqlO34QJBAOqpWb2jrJOlltN+67FpSxAue78+JiH7J+jULXN4k9cgt20gMMpoOu2GhTh0EgoXcDZHPW3NrpcQFWymDWXLLckCQQDSPHLBvMOaICkfs8Ofd1cTuw1BI7QNXIUKFvSU8rvwE1Z8SZkFhLPq+qIGxstADTXZdQx56dzMsUyqk/p2MvnPAkBzffwEAM1MMaBk4T+hJoBiK26ONklQSitfRSZFgZ/Jrnl4hPJefCQciSuCGGZUfyqkHDXYl/WItcrFmYhYhEI5AkAd7gEgV7E5Fe8E1mC5KRI6etyuM1kEtfEyuIXlVpEu4nHji86/HF9IypmagV6aJcdOx/0YthR7B5q0hhCYFzW9AkA3LfLhPfkzICKWxZRLNHFgMX6K60wvmekZMw3c4RlNOaWW8CsyjQ/vvCokP94UQGHXTVe+cvh6ZKoaoxHbmeUg'
    resp = query_order(partern=partern, order_id=out_trade_no, private_key=base64.decodestring(private_key))
    print resp
    parse_query_result(resp)