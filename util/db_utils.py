# -*- coding:utf-8 -*-

from database.core import DatabaseTemplate
from database.factory import OracleConnectionFactory
from util.config import PropertiesParser
import os.path


def get_datatemplate():
    props = PropertiesParser()
    config_file_name = os.path.join(os.path.dirname(__file__), 'epay.cfg')
    props.read(config_file_name)
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

