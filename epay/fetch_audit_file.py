# -*- coding: utf-8 -*-

#  Fetch audit file from payment org

from util import ssh_util

host = 'localhost'
username = 'user'
password = 'tyzF123!@#'

AUDIT_DIR = '/usr/local/epay/epay-platform/data/audit/bank/chinapaylfq'
INSTALMENT_FILE_PREFIX = 'TRAN_MER_SH-YJKJ-001000-0674-0009'
PREAUTH_INSTAMENT_FILE_PREFIX = 'TRAN_MER_SH-YJKJ-001000-0674-0010'
SUFFIX = 'txtend'

def fetch_audit_file(host, file_name, audit_date):
    client = ssh_util.SSHConnection(host=10722, username=username, password=password)
    client.exec_command()

if __name__ == '__main__':
    pass