# -*- coding:utf-8 -*-

from flask.blueprints import Blueprint
from flask import url_for, redirect
from werkzeug.security import check_password_hash
from flask.globals import request, g
from echo_telegram.echo_telegram_base import try_except, dao, app
from echo_telegram.app_logger import logger
from echo_telegram.api.signup import __get_user
from echo_telegram.db.user import User
from flask import session
from flask_login.login_manager import LoginManager
from flask_login.utils import login_user

login_api = Blueprint("login_api", __name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main_view.index'
# 보안성 레벨 설정
login_manager.session_protection = 'strong'
login_manager.login_message = '로그인이 필요함'


@login_manager.user_loader
@try_except
def load_user(userId):
    query = 'select user_id, name, rank, status, channel_id from users where user_id = %s'
    cursor = dao.get_conn().cursor()
    cursor.execute(query, [userId])
    current_user = cursor.fetchone()
    cursor.close()
    g.conn.commit()
    user = User(userId=current_user[0], name=current_user[1], rank=current_user[2], status=current_user[3],
                channel=current_user[4], auth=False)
    return None

@try_except
def check_pw(login_id, pw):
    query = '''select pw from users where id = %s'''
    cursor = dao.get_conn().cursor()
    cursor.execute(query, [login_id])
    db_pw = cursor.fetchone()
    return check_password_hash(db_pw[0], pw)


@login_api.route('/login', methods=['POST'])
def login():
    login_userId = request.form['login_id'].encode("utf-8")
    login_pw = request.form['login_pw'].encode("utf-8")

    user = __get_user(login_userId)

    if user:
        if check_pw(user[0], login_pw):
            print '1'
            user = User(userId=user[1].decode('utf-8'), name=user[2].decode('utf-8'), rank=user[3], status=None, channel=None, auth=False)
            print '2'
            login_user(user)
            print '3'
            session['userId'] = login_userId
            print '4'
            return redirect(url_for('dashboard_view.dashboard', user_id=login_userId))

    #로그인에 실패함
    return redirect(url_for('main_view.index'))