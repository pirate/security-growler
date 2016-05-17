#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Nick Sweeting (github.com/pirate) 2016
# MIT License

import traceback

from sources import get_new_lines
from parsers import parse_line, get_sources_info
from loggers import notify, alert

def watch_sources():
    """runloop to parse events from sources and dispatch alerts"""
    sources_info = '\n' + get_sources_info()
    first_line = True
    for source, line in get_new_lines():
        if first_line:
            first_line = False
            notify(sources_info, 'Started Watching Sources')

        # parse the fetched lines, if not alert-worthy, alert_type will be None
        alert_type, title, content = parse_line(line, source)

        if alert_type == 'notify':
            notify(content, title)

        if alert_type == 'alert':
            alert(content, title)

if __name__ == "__main__":
    try:
        watch_sources()
    except BaseException as e:
        if isinstance(e, Exception):
            notify(traceback.format_exc(), title='Stopped Watching Sources: %s' % type(e).__name__)
        else:
            notify('Quit by user: %s' % type(e).__name__, title='Stopped Watching Sources')
        raise
