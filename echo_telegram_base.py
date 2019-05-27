# -*- coding:utf-8 -*-

import sys
from flask.app import Flask
from app_logger import logger
from flask_session import Session
from functools import wraps
from flask.globals import g

reload(sys)
sys.setdefaultencoding("utf-8")

#flask 앱 생성
app = Flask(__name__)
logger.info("app 생성----------")

# 환경설정 파일들 경로 설정
from echo_telegram_conf import EchoTelegramConfig

app.config.from_object(EchoTelegramConfig)
logger.info(">>> app.confing : %s" % (str(app.config)))

#http 응답 끝날때 DB connection 닫기
@app.teardown_request
def db_close(e):
    if hasattr(g,"conn"):   #db_conntion이 있을 때만 close한다.
        #g.conn.commit()
        g.conn.close()
        logger.info( ">> db connection close - %s" % (g.conn))


# db 초기 설정값 입력
db_info = app.config['DB_USER']+':'+app.config['DB_PASSWD']+'@'+app.config['DB_HOST']+'/'+app.config['DB_SCHEMA']+'?charset=utf8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + db_info
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
session = Session(app)

# session 관리를 위한 테이블 자동생성
session.app.session_interface.db.create_all()

# 사용자 정의 데코레이터
def try_except(f):
    @wraps(f)
    def deco_func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.info("\n\n\n############exception############")
            logger.info(str(e))
            logger.info("#################################\n\n")
            raise e
    return deco_func

# db 초기화 후 dao객체 얻어오기
from db.EchoTelegramDB import EchoTelegramDB
db_url = 'mysql+pymysql://' + db_info
dao = EchoTelegramDB(db_url)
logger.info(">>> DB connection : %s" % (str(dao)))

# blueprint 등록
from views.main import main_view

app.register_blueprint(main_view)

logger.info(">>> Blueprint setting. ")
logger.info("===========================================================")
