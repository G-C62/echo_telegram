# -*- coding:utf-8 -*-

from flask.blueprints import Blueprint
from flask.globals import request, g
from flask.helpers import flash, url_for
from flask import redirect, jsonify
from werkzeug.security import generate_password_hash
from echo_telegram.echo_telegram_base import try_except, dao
from echo_telegram.app_logger import logger

signup_api = Blueprint("signup_api", __name__)

# user_id에 해당하는 계정이 있는지 확인하는 method
@try_except
def __get_user(user_id):
    logger.info('search_user_by id : '+user_id)
    query = '''select id, user_id, name, rank from users where user_id = %s'''
    cursor = dao.get_conn().cursor()
    #cursor.execute('set names utf8')
    cursor.execute(query, [user_id])
    current_user = cursor.fetchone()
    cursor.close()
    g.conn.commit()
    return current_user


@try_except
@signup_api.route("/sign_up", methods=['POST'])
def sign_up():
    id = request.values.get("signup_id").encode("utf-8") if "signup_id" in request.values else ''
    pw = request.values.get("signup_pw") if "signup_pw" in request.values else ''
    pw_check = request.values.get("signup_pw_check") if "signup_pw_check" in request.values else ''
    name = request.values.get("signup_name").encode("utf-8") if "signup_name" in request.values else ''
    rank = request.values.get("signup_rank").encode("utf-8") if "signup_rank" in request.values else ''


    logger.info('register_action data : ' + id + ', ' + name + ', ' + rank)
    hashed_pw = generate_password_hash(pw, salt_length=10)
    cursor = dao.get_conn().cursor()
    #cursor.execute('set names utf8')
    cursor.execute('''insert into users(user_id, pw, name, rank) values(%s, %s, %s, %s)''', [id, hashed_pw, name, rank])
    cursor.close()
    g.conn.commit()

    return redirect(url_for('main_view.index'))


# id중복검사
@try_except
@signup_api.route("/sign_up/check_id", methods=['POST'])
def check_id():
    user_id = request.json['user_id']
    if __get_user(user_id):
        return jsonify(result=False)
    else:
        return jsonify(result=True)
