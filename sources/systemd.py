"""Detect changes in systemd's journal"""

from __future__ import absolute_import
import select
try:
    from systemd import journal
except ImportError:
    raise Exception('You need the `python-systemd` library for Python 2.7. ' +
                    'See: https://github.com/systemd/python-systemd/')

def gen_lines():
    """generator which yields new lines from journalctl, or None"""
    j = journal.Reader()
    j.seek_tail()
    p = select.poll()
    p.register(j, j.get_events())
    yield 'ready'
    p.poll()
    while True:
        line = j.get_next()
        if line:
            yield str(line['SYSLOG_IDENTIFIER']) + ': ' + str(line['MESSAGE']).strip()
        else:
            yield None
