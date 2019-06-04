# -*- coding:utf-8 -*-

from flask.blueprints import Blueprint
from flask.globals import request, g
from flask.helpers import flash, url_for
from flask import redirect, jsonify
from flask_login import current_user
from echo_telegram_base import try_except, dao
from app_logger import logger

user_api = Blueprint("user_api", __name__)

@user_api.route('/update/location')
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
