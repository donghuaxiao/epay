# -*- coding:utf-8 -*-

from database.core import DatabaseTemplate
from database.factory import OracleConnectionFactory
from util.config import PropertiesParser

def get_datatemplate():
    props = PropertiesParser()
    props.read('epay.cfg')
    host = props.get_property('host')
    port = props.get_property('port')
    username = props.get_property('username')
    password = props.get_property("password")
    service = props.get_property('service')

    connect_factory = OracleConnectionFactory(host=host,
                                              username=username,
                                              password=password,
                                              port=port,
                                              service=service)
    dbtemplate = DatabaseTemplate(connect_factory)
    return dbtemplate

