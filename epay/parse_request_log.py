# -*- coding:utf-8 -*-

# parser request log file: requests.log, count request per seconds

import re
import copy


log_time_re = re.compile(r'\[\d{1,3}/\w+/\d{4}:(?P<time>.*) \+\d{4}\]')
log='10.252.117.83 -  -  [01/Aug/2017:00:46:19 +0800] "POST /epay?svc_cat=PayTx&svc_code=SetPayService HTTP/1.1" 200 909 "-" "Jakarta Commons-HttpClient/3.1"'


def parse_log(log):

    mg = log_time_re.search(log)
    return mg.group('time')


def count_log_by_sec(file_path):
    time_counts = {}

    with open(file_path, 'r') as f:
        for log in f:
            try:
                idx = log.index('DownPayOrgLogo')
                continue
            except ValueError as ex:
                pass
            time = parse_log(log)
            if time in time_counts:
                count = time_counts[time]
                count += 1
                time_counts[time] = count
            else:
                time_counts[time] = 1
    return time_counts


def write_file(orders, file_name):
    for order in orders:
        with open(file_name, 'w') as f:
            f.write("%s %s\n" % (order[0], order[1]))


def update_dict( dict1, dict2):
    new_dict = copy.deepcopy(dict1)
    for key,val in dict2.iteritems():
        if key in new_dict:
            count = new_dict[key] + val
            new_dict[key] = count
        else:
            new_dict[key] = val

    return new_dict

if __name__ == '__main__':

    time_counts_107 = count_log_by_sec('request_2017_08_01.log')
    max_count_107 = max(time_counts_107.values())
    print "107 max count: %s" % max_count_107
    for key, val in time_counts_107.iteritems():
        if val == max_count_107:
            print key

    time_counts_97 = count_log_by_sec('97_request_2017_08_01.log')
    max_count_97 = max(time_counts_97.values())
    print "97 max count: %s" % max_count_97
    for key, val in time_counts_97.iteritems():
        if val == max_count_97:
            print key

    time_counts_98 = count_log_by_sec('98_request_2017_08_01.log')
    max_count_98 = max(time_counts_98.values())
    print "98 max count: %s" % max_count_98
    for key, val in time_counts_98.iteritems():
        if val == max_count_98:
            print key

    new_dict = update_dict(time_counts_97, time_counts_107)
    new_dict = update_dict(new_dict, time_counts_98)

    max_count = max(new_dict.values())
    print "98 max count: %s" % max_count
    for key, val in new_dict.iteritems():
        if val == max_count:
            print key
