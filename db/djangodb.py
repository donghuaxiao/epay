# -*- coding:utf-8 -*-

from django.conf import settings

from django.db import connection

settings.configure(
    DATABASE_ENGINE="django.db.backends.oracle",
    DATABASE_HOST="localhost",
    DATABASE_NAME="tyzf",
    DATABASE_USER="epayment",
    DATABASE_PASSWORD="Epay789*QWE",
    DATABASE_PORT="15215"
)

with connection.cursor() as cursor:
    cursor.execute("select count(*) from t_audit_channel_file")
    result = cursor.fetchone()[0]
    print result