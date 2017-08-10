# -*- coding: utf-8 -*-
import datetime


NAME = "Logfile on desktop"
location = '/Users/squash/Desktop/security-growler.log'


def alert(title, body, level='INFO', time=None):
    with open(location, 'a') as outfile:
        if level == 'WARNING':
            outfile.write('[%s] %s: %s\n' % (timestamp(), title, body))
        else:
            outfile.write('[%s] ‼️ %s: %s\n' % (timestamp(), title, body))

def timestamp():
    return datetime.datetime.now().strftime('%m/%d %H:%M')
