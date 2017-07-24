# -*- coding:utf-8 -*-

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import base64
import json
import hashlib


def ras_sign_string(private_key, sign_string):
    key = RSA.importKey(private_key)
    singer = PKCS1_v1_5.new(key)
    signature = singer.sign(SHA.new(sign_string.encode('utf8')))
    sign = base64.encodestring(signature).encode("utf8").replace("\n", "")
    return sign


def rsa_verify(public_key, message, sign):
    key = RSA.importKey(public_key)
    signer = PKCS1_v1_5.new(key)
    digest = SHA.new()
    digest.update(message.encode("utf8"))
    if signer.verify(digest, base64.decodestring(sign.encode("utf8"))):
        return True
    return False


def sort_dict(data):
    complex_keys = []
    for key, value in data.items():
        if isinstance(value, dict):
            complex_keys.append(key)

    # 将字典类型的数据dump出来
    for key in complex_keys:
        data[key] = json.dumps(data[key], separators=(',', ':'))

    return sorted([(k, v) for k, v in data.items()])


def rsa_sign(private_key, params):
    sorted_params = sort_dict(params)
    unsigned_string = "&".join(["{}={}".format(k, v) for (k, v) in sorted_params])
    return ras_sign_string(private_key, unsigned_string)


def md5_sign_string(private_key, data):
    md5_str = data + private_key
    md5 = hashlib.md5()
    md5.update(md5_str)
    return md5.hexdigest()


def md5_sign(private_key, params):
    sorted_params = sort_dict(params)
    unsigned_string = "&".join(["{}={}".format(k, v) for (k, v) in sorted_params])
    return md5_sign_string(private_key, unsigned_string)

if __name__ == '__main__':
    md5_str = md5_sign("Tekoe1koej", {'service': 'single_query_order', 'order_id': '27870327'})
    print md5_str

