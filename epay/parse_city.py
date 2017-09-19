# -*- coding: utf-8 -*-

import xlsxwriter
import sys

reload(sys)
sys.setdefaultencoding('utf8')


if __name__ == '__main__':
    city_map = []
    with open('city.txt', 'r') as f:
        for line in f:
            items = line.split()
            city = [items[1], items[0], items[0][1:]]
            city_map.append(city)

    print city_map

    wb = xlsxwriter.Workbook(u'支付网关boss地市转换.xlsx')
    sheet = wb.add_worksheet(u'地市关系')
    sheet.write_row(0, 0, [u'地市', u'支付网关编码', u'boss编码'])
    idx = 1

    for city in city_map:
        sheet.write_row(idx, 0, city)
        idx += 1
    wb.close()