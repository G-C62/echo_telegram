# -*- coding:utf-8 -*-

from flask.blueprints import Blueprint
from flask.globals import request, g
from flask.helpers import flash, url_for
from flask import redirect, jsonify
from flask_login import current_user, login_required
from echo_telegram_base import try_except, dao
from app_logger import logger

user_api = Blueprint("user_api", __name__)

@user_api.route('/update/location')
@login_required
def update_location():
    user_location = request.args.get("location").encode("utf-8")
    # db에 가서 user정보 변경
    if user_location:
        cursor = dao.get_conn().cursor()
        cursor.execute('''update users set seat_location = %s 
                                where user_id = %s;''', [user_location, current_user.userId])
        cursor.close()
        g.conn.commit()

    return redirect(url_for('dashboard_view.dashboard'))


@user_api.route('/update/return')
@login_required
def return_seat():
    # status 수정
    cursor = dao.get_conn().cursor()
    cursor.execute('''update users set status = 'place' where user_id = %s;''',
                   [current_user.userId])
 #events의 iscompolete 수정
    cursor.execute('''update events set iscomplete = 1 where user_id = (select id from users where user_id = %s) 
                    and iscomplete = 0;''',
                   [current_user.userId])
    cursor.close()
    g.conn.commit()

    return redirect(url_for('dashboard_view.dashboard'))
