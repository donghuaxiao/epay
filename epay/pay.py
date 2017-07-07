#-*- coding:utf-8 -*-

import paramiko
import eventlet


def connect( host, username, password, port):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect( host, port, username, password)
    return client


def execute( client, command):
    stdin, stdout, err = client.exec_command( command)
    for line in stdout:
        print line

ports = [6522, 6622, 6722, 6822, 6922]
username = 'user'
password = 'tyzF123!@#'
host = 'localhost'
command = 'ps -ef | grep tomcat | grep -v grep'
for port in ports:
    client = connect(host, username, password, port)
    thread1 = eventlet.spawn(execute, client, command)
    restult = thread1.wait()
