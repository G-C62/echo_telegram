#-*-coding:utf-8-*-
from flask.globals import g
from sqlalchemy.engine import create_engine


class EchoTelegramDB:
    def __init__(self, url):
        self.engine = create_engine(url, encoding="utf8", pool_recycle=28000)

    def get_conn(self):
        if not hasattr(g, 'conn'):
            self.conn = self.engine.raw_connection()
            g.conn = self.conn
        return g.conn