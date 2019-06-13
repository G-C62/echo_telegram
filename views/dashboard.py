# -*- coding:utf-8 -*-


from flask.blueprints import Blueprint
from flask import render_template
from echo_telegram_base import try_except, dao
from app_logger import logger
from flask_login import login_required, current_user


dashboard_view = Blueprint("dashboard_view", __name__)


@dashboard_view.route('/dashboard')
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

    return render_template('dashboard.html', events=events)






