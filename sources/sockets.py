"""Detect changes in open connections on given TCP ports"""

import os

FAST_CMD = "netstat -tan | grep '[:.]{0}' | grep '{1}'"
LSOF_CMD = "sudo lsof +c 0 -i:{0} | grep -v '^launchd ' | grep '{1}'"

def get_details(port, state='ESTABLISHED'):
    get_conn_details = LSOF_CMD.format(port, state or '.*')

    return [
        details for details in os.popen(get_conn_details).read().strip().split('\n')
        if details.strip() and len(details.split()) > 9
    ]

def get_connections(port, state='ESTABLISHED'):
    """get list of active connections on a given port"""
    get_conn_list = FAST_CMD.format(port, state or '.*')
    return [
        line.strip().split()[3:]
        for line in os.popen(get_conn_list).read().strip().split('\n')
        if len(line.split()) > 5
    ]


def gen_conns(port):
    """generator which yields new connections on a port or None"""
    existing = get_connections(port)
    yield 'ready'    # otherwise it will hang until the first change appears

    while True:
        new = get_connections(port)
        if new and new != existing:
            existing = new
            for line in get_details(port):
                yield line or None
        else:
            yield None
