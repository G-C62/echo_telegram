# -*- coding:utf-8 -*-


from flask.blueprints import Blueprint
from flask.globals import request, g
from flask import render_template, url_for, redirect
from echo_telegram_base import try_except, dao
from app_logger import logger
from flask_login import login_required

dashboard_view = Blueprint("dashboard_view", __name__)


@dashboard_view.route('/dashboard')
@login_required
def dashboard():
    # 현재 사용자의 이벤트들을 select 해서 가져온 다음 넘겨줌
    cursor = dao.get_conn().cursor()
    cursor.execute(query, [login_id])
    db_pw = cursor.fetchone()


    return render_template('dashboard.html')






