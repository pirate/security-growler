#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Nick Sweeting (github.com/pirate) 2016
# MIT License

"""
./growler.py 5m
"""

import os
import sys
import signal
import traceback

from time import sleep
from datetime import datetime
from importlib import import_module
from multiprocessing import Process


def quit_handler(signo, _stack_frame=None):
    alert(
        level='INFO',
        title='Stopped Watching Sources',
        body='Quit by user: got signal #%s' % signo,
        time=datetime.now(),
    )
    raise SystemExit(0)

def import_files(folder):
    # all .py files in folder
    python_files = (
        fname for fname in os.listdir(folder)
        if fname.endswith('.py') and fname != '__init__.py'
    )
    # import each file and return the module
    return [
        import_module('{}.{}'.format(folder, fname[:-3]))
        for fname in python_files
    ]

def alert(**alert_kwargs):
    for logger in import_files('loggers'):
        logger.alert(**alert_kwargs)

def run_monitors(time_filter=None):
    procs = []
    # get monitors in parallel
    for monitor in import_files('monitors'):
        def collect_monitor_alerts():
            return monitor.run(time_filter)
        p = Process(target=collect_monitor_alerts)
        p.start()
        procs.append(p)

    # sort alerts by time
    alerts = [p.join() for p in procs]
    alerts = sorted(alerts, key=lambda a: a['time'])

    # send to each logger
    for alert_kwargs in alerts:
        alert(**alert_kwargs)

def main(continuous=True, time_filter='1d'):
    if continuous:
        while True:
            run_monitors(time_filter)
            sleep(58)    # TODO fix sloppy ~2sec gap of unseen alerts caused by script running time
    else:
        run_monitors(time_filter)


if __name__ == "__main__":
    try:
        time_filter = int(sys.argv[1])
    except Exception:
        time_filter = None

    signal.signal(signal.SIGTERM, quit_handler)
    try:
        main(continuous=not time_filter, time_filter=time_filter)
    except KeyboardInterrupt:
        quit_handler('CTRL-C')
    except SystemExit:
        raise
    except BaseException as e:
        # notify user protection has stopped at all costs, even if error is a SyntaxError
        alert(
            level='WARNING',
            title='Stopped Watching Sources: %s' % type(e).__name__,
            body=traceback.format_exc(),
        )
        raise
