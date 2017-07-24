# -*- coding:utf-8 -*-

class PayEngine(object):

    def __init__(self):
        pass

    def pay(self):
        pass

    def query_order(self, order_id, payment_order_id):
        raise NotImplemented

    def refund(self, order_id, payment_order_id):
        raise NotImplemented

    