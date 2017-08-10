# -*- coding: utf-8 -*-
"""Logger that outputs notifications to stdout"""

import datetime

def alert(title, body, level='INFO', time=None):
    if level == 'WARNING':
        warn(title, body, time)
    else:
        info(title, body, time)

def timestamp():
    return datetime.datetime.now().strftime('%m/%d %H:%M')

### Exported functions for use in the app
def info(title, body, time):
    print("[%s] %s: %s" % (time, title, body))

def warn(title, body, time):
    print("[%s] ‼️  %s: %s" % (time, title, body))
