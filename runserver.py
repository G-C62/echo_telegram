# -*- coding:utf-8 -*-

import sys
from echo_telegram_base import app

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    print "starting test server..."

    app.run(host='0.0.0.0', port=5000, debug=True)
