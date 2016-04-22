# -*- coding: utf-8 -*-
"""Logger that outputs notifications to a text logfile"""

import datetime

from settings import (
    EVENT_LOGFILE,
    INFO_TITLE,
    ALERT_TITLE,
)

def log(text, location=EVENT_LOGFILE):
    with open(location, 'a') as outfile:
        outfile.write(text + '\n')

def timestamp():
    return datetime.datetime.now().strftime('%m/%d %H:%M')

### Exported functions for use in the app
def notify(content, title=INFO_TITLE, icon=None):
    log('[%s] %s: %s' % (timestamp(), title, content))

def alert(content, title=ALERT_TITLE, icon=None):
    log('[%s] ‼️ %s: %s' % (timestamp(), title, content))
