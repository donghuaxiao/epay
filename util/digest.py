# -*- coding:utf-8 -*-

from Crypto.Cipher import DES3
from Crypto.Hash import MD5
from Crypto import Random

import base64


def digest(key, data):

    # iv = Random.new().read(DES3.block_size)
    cipher = DES3.new(key, DES3.MODE_ECB)
    encrypt_data = cipher.encrypt(data)
    h = MD5.new(encrypt_data)
    md5_data = h.digest()
    return base64.encodestring(md5_data)

if __name__ == '__main__':

    c_idWeb = "01"

    o_idWeb = "20130614121234"

    o_timeWeb = "20130614121234"

    merchant = "010100GD001"

    user = "13926405877"

    puser = None

    point = '0'

    amount = '10'

    pswdWeb = "BBDmwTjBsF7IwTIyGWt1bmFn"

    originWeb = c_idWeb + "," + o_idWeb + "," + o_timeWeb + "," + merchant + "," + user + "," + "," + point + "," + amount + ","
    print originWeb
    print len(originWeb)

    print digest(pswdWeb, originWeb)

