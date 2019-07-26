# -*- coding:utf-8 -*-


from flask.blueprints import Blueprint
from flask import url_for, redirect, request, g, flash
from echo_telegram_base import dao, try_except, app
from flask_login import current_user, login_required
import telegram
import schedule
import datetime


echo_api = Blueprint("echo_api", __name__)

def start_event(category, name):
    # 참석자 및 등록한 사람 status 변경
    with app.app_context():
        insert_name = name if name != None else current_user.name
        cursor = dao.get_conn().cursor()
        cursor.execute('''update users set status = %s where name = %s;''', [category, insert_name])

    return schedule.CancelJob

@echo_api.route('/echo', methods=['POST'])
@try_except
@login_required
def create_event():
    #telegram bot 생성
    channel = request.form['event_channel'].encode("utf-8") if 'event_channel' in request.form else ''
    chat_id = '@' + channel

    my_token = '679610515:AAFtEx0IjBlLQAobCva70CBrqgyYpOrcEDU'  # 토큰을 설정해 줍니다.

    bot = telegram.Bot(token=my_token)  # 봇을 생성합니다.

    category =  request.form['event_category'].encode("utf-8") if 'event_category' in request.form else ''
    location =  request.form['event_location'].encode("utf-8") if 'event_location' in request.form else ''
    subject =  request.form['event_subject'].encode("utf-8") if 'event_subject' in request.form else ''
    attendants =  request.form['event_attendants'].encode("utf-8") if 'event_attendants' in request.form else ''
    start =  request.form['event_start'].encode("utf-8") if 'event_start' in request.form else ''
    query = ''

    # status가 존재하는데 또 생성하려는 경우 방지
    if current_user.status != 'place' and current_user.status is not None and category != 'notice':
        flash('자리에 돌아온 후 다시 시도해주세요')
        return redirect(url_for('dashboard_view.dashboard'))

    #start가 pm이면 12시간 더해주기
    if 'PM' in start:
        hour = str(int(start[0:2])+12)
        minute = start[2:5]
        start = hour + minute

    cursor = dao.get_conn().cursor()
    #DB에 이벤트 insert
    if category == 'meeting':
        query = '''insert into events(category, place, subject, start_time, channel_id, user_id, attendants) 
                    values(%s, %s, %s, %s, %s, (select id from users where user_id = %s), %s)'''
        cursor.execute(query, [category, location, subject, start, current_user.channel, current_user.userId, attendants])
        # bot.sendMessage(chat_id=chat_id, text='---- 회의 -----\n' +
        #                                         '장소: ' + location + '\n' +
        #                                         '주제: ' + subject + '\n' +
        #                                         '참석자: ' + attendants + '\n' +
        #                                         '시작시간: ' + start + '\n' +
        #                                         '** 작성자  :' + current_user.name)  # 메세지를 보냅니다.
    elif category == 'away' or category == 'outside':
        query = '''insert into events(category, subject, start_time, channel_id, user_id) 
                            values(%s, %s, %s, %s, (select id from users where user_id = %s))'''
        cursor.execute(query, [category, subject, start, current_user.channel, current_user.userId])
        if category == 'away':
            pass
             # bot.sendMessage(chat_id=chat_id, text='---- 자리비움 -----\n' +
             #                                    '사유: ' + subject + '\n' +
             #                                    '시작시간: ' + start + '\n' +
             #                                    '** 작성자  :' + current_user.name)  # 메세지를 보냅니다.
        else:
            pass
             # bot.sendMessage(chat_id=chat_id, text='---- 외근 -----\n' +
             #                                        '주제: ' + subject + '\n' +
             #                                        '시작시간: ' + start + '\n' +
             #                                        '** 작성자  :' + current_user.name)  # 메세지를 보냅니다.
    elif category == 'notice':
        query = '''insert into events(category, channel_id, user_id, attendants, iscomplete) 
                            values(%s, %s, (select id from users where user_id = %s), %s, 1)'''
        cursor.execute(query, [category, current_user.channel, current_user.userId, attendants])
        # bot.sendMessage(chat_id=chat_id, text='---- 공지 -----\n' +
        #                                        attendants + '\n' +
        #                                        '** 작성자  :' + current_user.name)  # 메세지를 보냅니다.
        return redirect(url_for('dashboard_view.dashboard'))
    else:
        return redirect(url_for('dashboard_view.dashboard'))

    cursor.close()
    g.conn.commit()

    #schedule 걸어서 해당 시간되면 참석자 및 작성자 status변화 시키기
    # 1. 현재시간보다 이전 시간인 경우
    now = datetime.datetime.now()
    start_datetime = now.replace(hour=int(start[0:2]), minute=int(start[3:5]))
    if now > start_datetime:
        if category == 'meeting':
            # 공백 또는 , 로 분할하여 리스트로만듦
            attendants_list = attendants.replace(' ', '').split(',') if ',' in attendants else attendants.split(' ')
            # 참석자 수만큼 돌려서 update
            for i in range(len(attendants_list)):
                start_event(category, attendants_list[i])

        start_event(category, current_user.name)

    # 2. 현재시간 이후인 경우
    else:
        if category == 'meeting':
            # 공백 또는 , 로 분할하여 리스트로만듦
            attendants_list = attendants.replace(' ', '').split(',') if ',' in attendants else attendants.split(' ')
            # 참석자 수만큼 돌려서 update
            for i in range(len(attendants_list)):
                schedule.every().day.at(start[0:5]).do(start_event, category=category, name=attendants_list[i])

        schedule.every().day.at(start[0:5]).do(start_event, category=category, name=current_user.name)

    cursor.close()
    g.conn.commit()

    return redirect(url_for('dashboard_view.dashboard'))