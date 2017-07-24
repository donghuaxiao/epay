# -*- coding:utf-8 -*-

import xml.etree.ElementTree as ET
from pay.certsupport import alipaysupport


def get_node_text(node):
    for text_node in node.childNodes:
        if text_node.nodeType == node.TEXT_NODE:
            return text_node.data
    return None


def parse_node(node):
    data = {}
    for child in node:
        tag = child.tag
        if tag == 'param':
            tag = child.get('name')
        childs = list(child)
        if len(childs) > 0:
            data[tag] = parse_node(child)
        else:
            data[tag] = child.text
    return data

if __name__ == '__main__':
    doc = ET.parse("query_result_success.xml")
    root = doc.getroot()
    resp = parse_node(root)
    data = resp['response']['trade']
    print data
    sorted_params = alipaysupport.sort_dict(data)
    sign_string = '&'.join(['%s=%s' % (k,v) for (k,v) in sorted_params])
    print sign_string


