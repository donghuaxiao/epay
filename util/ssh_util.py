import paramiko

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
