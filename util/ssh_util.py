# -*- coding: utf-8 -*-

import paramiko
import os.path
import ntpath

from util import exceptions

class SSHConnection(object):

    def __init__(self, host, username, password, port=22):
        self._host = host
        self._username = username
        self._password = password

        self._port = port
        # init SSHClients
        self._client = self._create_ssh_connection()

    def _create_ssh_connection(self):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self._host, port=self._port, username=self._username, password=self._password)
            print "create a connection"
            return client
        except paramiko.SSHException as e:
            print e
            return None

    def exec_command(self, command):
        print "run command: %s" % command
        stdin, stdout, stderr = self._client.exec_command(command)
        return stdout.read().splitlines()

    def put_file(self, in_path, out_path):
        print "put file %s from local to %s %s" % (in_path, self._host, out_path)

        if not os.path.exists(in_path):
            raise exceptions.FileNotFoundException('%s is not exists' % in_path)

        try:
            self.sftp = self._client.open_sftp()
            self.sftp.put(in_path, out_path)
        except Exception as e:
            print e
            raise exceptions.SSHException("failed to transfer file to %s" % out_path)

    def get_file(self, in_path, out_path):
        print
if __name__ == '__main__':
    ssh_client = SSHConnection(host='192.168.10.13', username='root', password='password')
    in_file = os.path.join(os.path.dirname(__file__), 'mail_util.py')
    print os.path.exists(ntpath.dirname(__file__))
    out_file = '/root/mail_util.py'
    ssh_client.put_file(in_file, out_file)