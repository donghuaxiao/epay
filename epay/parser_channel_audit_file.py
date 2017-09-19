# -*- coding:utf-8 -*-

from __future__ import division

def parse_audit_log( audit_file ):
    success_audit_record = []
    with open(audit_file, 'r') as f:

        f.readline() #skip first line
        for line in f:
            items = line.split('\t')
            status = items[10]
            print status
            if int(status) == 2:
                success_audit_record.append(items)
    return success_audit_record


def account_audit_log( audits ):
    amount = 0
    for audit in audits:
        amount += (int(audit[6]) / 100)
    return amount


def parse_audit_header( audit_header_line):
    head_items = audit_header_line.split('\t')
    return {'start_time': head_items[0],
            'end_time': head_items[1],
            'count': head_items[2]}


def parse_audit_file( file_name ):
    audit = {}
    audit_records = {}
    with open(file_name, 'r') as f:
        audit_header_line = f.readline()
        audit['head'] = parse_audit_header(audit_header_line)
        for audit_record_line in f:
            audit_items = audit_record_line.split('\t')
            audit_records[ audit_items[5]] = [audit_items[4], audit_items[6], audit_items[10]]
    audit['audit_records'] = audit_records
    return audit


def diff_record(r1, r2):
    for order_id, audit_record in r1.iteritems():
        audit_record_dest = r2.get(order_id)
        if audit_record_dest is None:
            print "order_id %s different" % order_id
            continue
        diff = True
        if len(audit_record) == len(audit_record_dest):
            for i in range(len(audit_record)):
                if audit_record[i] != audit_record_dest[i]:
                    diff = False
                    break
        else:
            diff = False
        if diff is False:
            print "order_id %s different" % order_id


def diff_audit_file( file_src, file_dest):
    audit_record_src = parse_audit_file(file_src)
    audit_record_dest = parse_audit_file(file_dest)

    diff_record(audit_record_src.get('audit_records'), audit_record_dest.get('audit_records'))


if __name__ == '__main__':
    # file_name = ''
    # audits = parse_audit_log(file_name)
    # for audit in audits:
    #     print audit[5]
    # amount = account_audit_log(audits)
    # print amount

    diff_audit_file( '02_audit_20170825.txt', '02_audit_20170828.txt')