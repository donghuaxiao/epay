# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

oracle_dns = 'epayment/Epay789*QWE@localhost:15215/tyzf'
oracle_url = 'oracle://epayment:Epay789*QWE@localhost:15215/tyzf1'
engine = create_engine(oracle_url, echo=True)


result = engine.execute('select count(*) from t_audit_channel_file')
for rowproxy in result:
    print rowproxy[0]
result.close()