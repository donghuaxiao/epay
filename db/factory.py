# -*- coding:utf-8 -*-


class ConnectionFactory(object):
    def __init__(self, host, username, password, database=None, port=None):
        self._host = host
        self._username = username
        self._password = password
        self._database = database
        self._port = port

    def get_connection(self):
        raise NotImplemented


class OracleConnectionFactory(ConnectionFactory):

    def __init__(self, host, username, password, database=None,  service=None, sid=None, port=1521):
        super(OracleConnectionFactory, self).__init__(host, username, password, database, port)
        self._service = service
        self._sid = sid

        self._connect_url = "%s/%s@%s:%s/%s" % (self._username, self._password, self._host, self._port, self._service)

    def get_connection(self):
        import cx_Oracle as ora
        return ora.connect(self._connect_url)
