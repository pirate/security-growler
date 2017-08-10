# -*- coding: utf-8 -*-
"""Logger that outputs notifications to stdout"""

import datetime

from settings import (
    INFO_TITLE,
    ALERT_TITLE,
)

def timestamp():
    return datetime.datetime.now().strftime('%m/%d %H:%M')

### Exported functions for use in the app
def notify(content, title=INFO_TITLE, icon=False):
    print("[%s] %s: %s" % (timestamp(), title, content))

def alert(content, title=ALERT_TITLE, icon=False):
    print("[%s] ‼️  %s: %s" % (timestamp(), title, content))
