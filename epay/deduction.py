# -*- coding:utf-8 -*-

from util import ssh_util

cmd = 'java test.VerifyBankAccountThread 1 00 A 44082319820102003X 28 4367423324180602239 吴仁光 05 jhwl null 44001400046052500513 10.252.42.107 5000'

conn = ssh_util.SSHConnection(host='localhost', username='user', password='tyzF123!@#', port=10722)
results = conn.exec_command("ls -l")
for line in results:
    print line