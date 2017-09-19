# -*- coding:utf-8 -*-

import re

log_time_re = re.compile(r'\[\d{1,3}/\w+/\d{4}:(?P<time>.*) \+\d{4}\]')

def parse_log(log):

    mg = log_time_re.search(log)
    return mg.group('time')


if __name__ == '__main__':
    with open('file093338.txt', 'w') as af:
        with open('97_request_2017_08_01.log', 'r') as f:
            for log in f:
                if parse_log(log) == '09:33:38':
                    af.write(log)
