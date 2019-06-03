# -*- coding: utf-8 -*-
from flask_login import login_required, current_user
from flask import redirect, url_for, Blueprint, request, g
from echo_telegram.echo_telegram_base import dao

register_channel_api = Blueprint("register_channel_api", __name__)


@register_channel_api.route('/register_channel')
@login_required
def register_channel():
    # prompt로 보내온 채널ID를 DB에 등록 한 후
    # 현재 유저의 채널로 설정
    # 이후 dashboard로 다시 이동
    channel_id = request.args.get("channel").encode("utf-8") if "signup_id" in request.values else ''
    cursor = dao.get_conn().cursor()
    cursor.execute('''insert into channels(channel_name) values(%s)''', [channel_id])
    cursor.close()
    g.conn.commit()

    cursor = dao.get_conn().cursor()
    cursor.execute('''update users set channel_id = %s where user_id = %s''', [channel_id, current_user.userId])
    cursor.close()
    g.conn.commit()

    return redirect(url_for('dashboard_view.dashboard'))