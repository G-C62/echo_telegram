# -*- coding: utf-8 -*-


class EchoTelegramConfig(object):
    SECRET_KEY = "3PO-Echo"
    SESSION_SQLALCHEMY_TABLE = "sessions"
    SESSION_TYPE = "sqlalchemy"
    DB_USER = "root"
    DB_PASSWD = "webdev1!"
    DB_HOST = "10.10.1.175"
    DB_SCHEMA = "c62"

