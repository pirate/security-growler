"""Detect changes in systemd's journal"""

from __future__ import absolute_import
import select
from systemd import journal

def gen_lines():
    """generator which yields new lines from journalctl, or None"""
    j = journal.Reader()
    j.seek_tail()
    p = select.poll()
    p.register(j, j.get_events())
    p.poll()
    while True:
        line = j.get_next()
        if line:
            yield str(line['SYSLOG_IDENTIFIER']) + ': ' + str(line['MESSAGE']).strip()
        else:
            yield None
