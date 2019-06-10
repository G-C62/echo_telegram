# -*- coding:utf-8 -*-


from flask.blueprints import Blueprint
from flask import url_for, redirect, request


echo_api = Blueprint("echo_api", __name__)

@echo_api.route('/echo', methods=['POST'])
def create_event():
   # print request.form['event_category']
    print request.form['event_location'].encode("utf-8")
    print request.form['event_subject'].encode("utf-8")
    print request.form['event_attendants'].encode("utf-8")
    print request.form['event_start'].encode("utf-8")

   # PM일 경우에만 시간에 12를 더해주면 될듯

    return redirect(url_for('dashboard_view.dashboard'))