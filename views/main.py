#-*- coding:utf-8 -*-
from flask.templating import render_template
from flask.blueprints import Blueprint

main_view = Blueprint("main_view", __name__)


@main_view.route("/")
def index():
    return render_template("/index.html")