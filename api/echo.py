# -*- coding:utf-8 -*-


from flask.blueprints import Blueprint
from flask import url_for, redirect, request, g
from echo_telegram_base import dao, try_except
from flask_login import current_user
import telegram
from telegram.utils.request import Request

echo_api = Blueprint("echo_api", __name__)



@echo_api.route('/echo', methods=['POST'])
@try_except
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
        bot.sendMessage(chat_id=chat_id, text='---- 회의 -----\n' +
                                              '장소: ' + location + '\n' +
                                              '주제: ' + subject + '\n' +
                                              '참석자: ' + attendants + '\n' +
                                              '시작시간: ' + start + '\n' +
                                              '** 작성자  :' + current_user.name)  # 메세지를 보냅니다.
    elif category == 'away' or category == 'outside':
        query = '''insert into events(category, subject, start_time, channel_id, user_id) 
                            values(%s, %s, %s, %s, (select id from users where user_id = %s))'''
        cursor.execute(query, [category, subject, start, current_user.channel, current_user.userId])
        if category == 'away':
            bot.sendMessage(chat_id=chat_id, text='---- 자리비움 -----\n' +
                                              '사유: ' + subject + '\n' +
                                              '시작시간: ' + start + '\n' +
                                              '** 작성자  :' + current_user.name)  # 메세지를 보냅니다.
        else:
            bot.sendMessage(chat_id=chat_id, text='---- 외근 -----\n' +
                                                  '주제: ' + subject + '\n' +
                                                  '시작시간: ' + start + '\n' +
                                                  '** 작성자  :' + current_user.name)  # 메세지를 보냅니다.
    elif category == 'notice':
        query = '''insert into events(category, channel_id, user_id, attendants) 
                            values(%s, %s, (select id from users where user_id = %s), %s)'''
        cursor.execute(query, [category, current_user.channel, current_user.userId, attendants])
        bot.sendMessage(chat_id=chat_id, text='---- 공지 -----\n' +
                                              '내용: ' + attendants + '\n' +
                                              '** 작성자  :' + current_user.name)  # 메세지를 보냅니다.
    else:
        return redirect(url_for('dashboard_view.dashboard'))

    cursor.close()
    g.conn.commit()

    #schedule 걸어서 해당 시간되면 참석자 및 작성자 status변화 시키기
    return redirect(url_for('dashboard_view.dashboard'))