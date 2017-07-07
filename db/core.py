# -*- coding: utf-8 -*-

import cx_Oracle

RESULT_TYPE_DICT = 'DICT_TYPE'
RESULT_TYPE_TUPLE = 'LIST_TYPE'

def makedict(cursor):
    cols = [d[0].lower() for d in cursor.description]

    def createrow(*args):
        return dict(zip(cols, args))

    return createrow


def output_type_handler(cursor, name, default_type, size, precision, scale):
    if default_type in (cx_Oracle.STRING, cx_Oracle.FIXED_CHAR):
        return cursor.var(unicode, size, cursor.arraysize)
    if default_type == cx_Oracle.BLOB:
        return cursor.var(cx_Oracle.LONG_BINARY, 80000, cursor.arraysize)
    if default_type == cx_Oracle.CLOB:
        return cursor.var(cx_Oracle.LONG_STRING, 80000, cursor.arraysize)


class DbTemplate(object):
    def __init__(self, connect_factory):
        self.connect_factory = connect_factory

    def query_list(self, sql, params=None, outputtypehandler=None, row_factory=None, result_type=None):
        conn = self.connect_factory.get_connection()
        if outputtypehandler is not None:
            conn.outputtypehandler = output_type_handler
        try:
            cur = conn.cursor()
            if params is not None:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
            cur.rowfactory = makedict(cur)
            results = cur.fetchall()
            return [row for row in results]

        except Exception as ex:
            print ex.message
            return None
        finally:
            conn.close()

    def _query_list(self, sql, params=None):
        conn = self.connect_factory.get_connection()
        try:
            cur = conn.cursor()
            if params is not None:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
            result = cur.fetchall()
            return [rs for rs in result]
        except Exception as ex:
            print ex.message
            return None
        finally:
            conn.close()

    def query_for_int(self, sql, params=None):
        results = self._query_list(sql, params)
        retval = results[0][0]
        try:
            retval = int(retval)
            return retval
        except Exception as ex:
            print ex.message

    def query_for_object(self, sql, params):
        results = self._query_list(sql, params)
        return results[0][0]

