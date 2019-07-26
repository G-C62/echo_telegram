# -*- coding:utf-8 -*-


from flask.blueprints import Blueprint
from flask import render_template, request, jsonify
from echo_telegram_base import try_except, dao
from app_logger import logger
from flask_login import login_required, current_user
import json
from datetime import timedelta


dashboard_view = Blueprint("dashboard_view", __name__)


@dashboard_view.route('/dashboard',  methods=['POST', 'GET'])
@try_except
@login_required
def dashboard():
    # 현재 사용자의 이벤트들을 select 해서 가져온 다음 넘겨줌
    cursor = dao.get_conn().cursor()
    cursor.execute('''
                    select users.user_id,rank, status, name, seat_location, events.user_id, category, place, 
                    subject, start_time, attendants, channel_name, iscomplete
                    from users left join channels
                    on users.channel_id = channels.id
                    left join events 
                    on users.id = events.user_id 
                    and iscomplete = 0
                    where users.channel_id = %s;
                    ''', [current_user.channel])
    events = [dict((cursor.description[idx][0], value)
                  for idx, value in enumerate(row)) for row in cursor.fetchall()]

    for event in events:
        if event['attendants'] is not None:

            attendants_text = event['attendants'].replace('\r\n', '||')
            event['attendants'] = attendants_text

    # if request.get == reload 면 json으로 response 보내기
    if request.method == 'POST':
        # events 돌면서 time 들어가는 속성들 문자열로 바꿔주기

        for event in events:
            for key, value in event.items():
                if type(value) is timedelta:
                    event[key] = unicode(str(value), 'utf-8')
        return jsonify(result=events)

    return render_template('dashboard.html', events=events)






