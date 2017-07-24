# -*- coding: utf-8 -*-

import re
import db_utils

from util import ssh_util

cmd = "grep ackNotif /usr/local/epay/epay-platform/logs/dispatch.log.%s | grep error"

message_regex = re.compile('messageId=(?P<messageId>\d+)')

host = 'localhost'
username = 'user'
password = 'tyzF123!@#'


def grep_update_notify_failure(port, log_date):
    client = ssh_util.SSHConnection(host=host, username=username, password=password, port=port)
    logs = client.exec_command(cmd % log_date)

    message_ids = []
    for log in logs:
        match = re.search(message_regex, log)
        message_ids.append(match.group('messageId').strip())
    return message_ids

if __name__ == '__main__':
    log_date = '2017-07-23'
    ids_1 = grep_update_notify_failure(port=9722, log_date=log_date)
    print len(ids_1)
    ids_2 = grep_update_notify_failure(port=9822, log_date=log_date)
    print len(ids_2)
    ids_3 = grep_update_notify_failure(port=10722, log_date=log_date)
    print len(ids_3)

    ids_1.extend(ids_2)
    ids_1.extend(ids_3)

    sql = """
    SELECT MESSAGE_ID
    FROM T_MESSAGE
    WHERE MESSAGE_ID IN ( %s ) AND STATUS != 2
    """
    ids = "'" + "','".join(ids_1) + "'"

    dbtemplate = db_utils.get_datatemplate()

    results = dbtemplate.query_list(sql % ids)
    message_ids = [[res[0]] for res in results]


    update_sql = """
    UPDATE T_MESSAGE SET STATUS = 2 WHERE MESSAGE_ID = :1
    """
    if len(message_ids) != 0:
        row_affected = dbtemplate.update(update_sql, message_ids)
        print "row_affected: %s" % row_affected
    else:
        print "no record need to update"







