# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def connect_mail_server(host, port, sender, password):
    try:
        smtp = smtplib.SMTP(host,port)
        smtp.login(sender, password)
        return smtp
    except Exception as ex:
        print ex
        return None


def send_mail(host=None, port=None, sender=None, password=None, receiver=None, subject=None, body=None, files=[]):
    smtp = connect_mail_server(host, port, sender, password)
    if smtp is None:
        return

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ';'.join(receiver)
    msg['Subject'] = subject
    msg.attach(MIMEText(body))

    for filename in files:
        part = MIMEBase('application', 'octext-stream')
        part.set_payload(open(filename, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attach; filename=%s' % filename)
        msg.attach(part)

    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.close()


if __name__ == '__main__':
    host = 'smtp.163.com'
    port = 25
    sender = 'x_donghua@163.com'
    password = 'xdhua850920'
    receiver = ['392994631@qq.com', 'donghua.xiao@ericsson.com']

    subject = u'测试邮件'
    body = u'test test test test test test'

    attach_file = ['24_201706.xlsx']

    send_mail(host, port, sender, password,receiver,subject=subject, body=body, files=attach_file)


