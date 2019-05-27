# -*- coding:utf-8 -*-

import sys, os
from flask.app import Flask

reload(sys)
sys.setdefaultencoding("utf-8")

#flask 앱 생성
app = Flask(__name__)