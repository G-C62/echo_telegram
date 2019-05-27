import os, sys
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
sys.path.insert(0, '/home/c62/flask_project/echo_telegram/')
from echo_telegram_base import app as application