# -*- coding:utf-8 -*-


from flask.blueprints import Blueprint
from flask import url_for, redirect
from werkzeug.security import check_password_hash
from flask.globals import request, g
from echo_telegram_base import try_except, dao, app
from app_logger import logger
from api.signup import __get_user
from db.user import User
from flask import session
from flask_login.utils import login_user, login_required, logout_user



login_api = Blueprint("login_api", __name__)


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
            user = User(userId=user[1].decode('utf-8'), name=user[2].decode('utf-8'), rank=user[3], status=None\
                        , channel=None, location=None, auth=False)
            login_user(user)
            session['userId'] = login_userId
            return redirect(url_for('dashboard_view.dashboard'))

    #로그인에 실패함
    return redirect(url_for('main_view.index'))


@login_api.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_view.index'))