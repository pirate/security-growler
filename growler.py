#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Nick Sweeting (github.com/pirate) 2016
# MIT License

import signal
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


def quit_handler(signo, _stack_frame=None):
    notify('Quit by user: got signal #%s' % signo, title='Stopped Watching Sources')
    raise SystemExit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, quit_handler)
    try:
        watch_sources()
    except KeyboardInterrupt:
        quit_handler('CTRL-C')
    except SystemExit:
        raise
    except BaseException as e:
        # notify user protection has stopped at all costs, even if error is a SyntaxError
        notify(traceback.format_exc(), title='Stopped Watching Sources: %s' % type(e).__name__)
        raise
