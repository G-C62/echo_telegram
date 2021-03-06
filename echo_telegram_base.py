# -*- coding:utf-8 -*-

import sys, os
from flask import Flask, current_app
from app_logger import logger
from flask_session import Session
from functools import wraps
from flask.globals import g, request
from datetime import datetime, timedelta
from flask_login.login_manager import LoginManager

import schedule
import time
from threading import Thread



login_manager = LoginManager()
login_manager.login_view = 'main_view.index'
# 보안성 레벨 설정
login_manager.session_protection = 'strong'
login_manager.login_message = '로그인이 필요함'

reload(sys)
sys.setdefaultencoding("utf-8")



#flask 앱 생성
app = Flask(__name__)


with app.app_context():



    logger.info("app 생성----------")

    # 환경설정 파일들 경로 설정
    from echo_telegram_conf import EchoTelegramConfig

    app.config.from_object(EchoTelegramConfig)
    logger.info(">>> app.confing : %s" % (str(app.config)))

    login_manager.init_app(app)
    logger.info("login_manager init----------------")

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

    # session 유지 시간설정
    app.permanent_session_lifetime = timedelta(days=31)

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

    from db.user import User

    @login_manager.user_loader
    @try_except
    def load_user(userId):
        query = 'select user_id, name, rank, status, channel_id, seat_location from users where user_id = %s'
        cursor = dao.get_conn().cursor()
        cursor.execute(query, [userId])
        current_user = cursor.fetchone()
        cursor.close()
        g.conn.commit()
        user = User(userId=current_user[0], name=current_user[1], rank=current_user[2], status=current_user[3],
                    channel=current_user[4], location=current_user[5], auth=False)
        return user

    # blueprint 등록
    from api.login import login_api
    from views.main  import main_view
    from views.dashboard import dashboard_view
    from api.signup import signup_api
    from api.register_channel import register_channel_api
    from api.user import user_api
    from api.echo import echo_api

    app.register_blueprint(login_api)
    app.register_blueprint(main_view)
    app.register_blueprint(dashboard_view)
    app.register_blueprint(signup_api)
    app.register_blueprint(register_channel_api)
    app.register_blueprint(user_api, url_prefix='/user')
    app.register_blueprint(echo_api)



    # thread생성
    def run_schedule():
        while 1:
            schedule.run_pending()
            time.sleep(1)


    thread = Thread(target=run_schedule)
    thread.daemon = True
    thread.start()



    # 로그인 페이지 엔드포인트

    logger.info(">>> Blueprint setting. ")
    logger.info("===========================================================")
