import datetime
from Crypto.Cipher import AES
from flask import request, g
from Crypto import Random
import binascii


def parse_to_dict(data):
    r = {}
    ignored_global_keys = [
        '_sa_instance_state'
    ]

    for key, value in data.__dict__.items():
        if value not in ignored_global_keys:
            r[key] = sanitize_value(value)
    return r


def sanitize_value(value):
    if type(value) is datetime.datetime:
        return str(value)
    return value


class PyCrypto247:
    def __init__(self, key):
        self.key = key
        self.pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        self.un_pad = lambda s: s[0:-s[-1]]

    def encrypt(self, raw):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        enc = (iv + cipher.encrypt(raw))
        enc = binascii.b2a_hex(enc)
        return enc.decode('utf-8')

    def decrypt(self, enc):
        enc = binascii.a2b_hex(enc)
        iv = enc[:16]
        enc = enc[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.un_pad(cipher.decrypt(enc)).decode('utf-8')


def log(item_id=None):
    from app.models.log import Log

    l = Log(user_id=g.user.id, action='{0}'.format(request.endpoint))
    if item_id:
        l.item_id = item_id
    l.create()
