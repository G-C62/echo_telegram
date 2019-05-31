# -*- coding:utf-8 -*-

from flask.blueprints import Blueprint
from flask.globals import request, g
from flask import render_template, url_for
from echo_telegram.echo_telegram_base import try_except, dao
from echo_telegram.app_logger import logger
from flask_login import login_required

dashboard_view = Blueprint("dashboard_view", __name__)


@dashboard_view.route('/dashboard/<user_id>')
def dashboard(user_id):
    return render_template('dashboard.html', user_id=user_id)
