# -*- coding:utf-8 -*-

import calendar as cal


def print_parition_stat(year, month, days):
    day_spec = '%s%s%s'
    if month < 10:
        month = '0%s' % month
    with open('partition_stat2017.txt', 'a') as f:
        for day in range(1, days):
            if day < 10:
                day = '0%s' % day
            partition_day = day_spec % (year, month, day)
            f.write('PARTITION PAYMENT_ORDER_%s VALUES LESS THAN(%s),\n' % (partition_day,partition_day))


def generate_partition_sql():
    year = 2017
    for m in range(1, 9):
        d = cal.monthrange(year, m)
        print_parition_stat(year, m, d[1])


if __name__ == '__main__':
    generate_partition_sql()