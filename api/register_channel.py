# -*- coding: utf-8 -*-
from flask_login import login_required, current_user
from flask import redirect, url_for, Blueprint, request, g
from echo_telegram_base import dao

register_channel_api = Blueprint("register_channel_api", __name__)


def check_channel(channel):
    cursor = dao.get_conn().cursor()
    cursor.execute('''select * from channels where channel_name = %s''', [channel])
    result = False if cursor.fetchone() is not None else True
    cursor.close()
    g.conn.commit()
    return result


@register_channel_api.route('/register_channel')
@login_required
def register_channel():
    # prompt로 보내온 채널ID를 DB에 등록 한 후
    # 현재 유저의 채널로 설정
    # 이후 dashboard로 다시 이동
    channel_id = request.args.get("channel").encode("utf-8")
    cursor = dao.get_conn().cursor()
    if(check_channel(channel_id)):
        cursor.execute('''insert into channels values(null, %s);''', [channel_id])
    cursor.execute('''update users set channel_id = (select id from channels where channel_name = %s) 
                        where user_id = %s;''', [channel_id, current_user.userId])
    cursor.close()
    g.conn.commit()

    return redirect(url_for('dashboard_view.dashboard'))