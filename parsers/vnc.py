from .connections import parse_connection

TITLE = 'VNC CONNECTED {0}'
BODY = 'To: {0} {1} ({2}) -> {3}'

def parse(line, source=None):
    conn = parse_connection(line, source)
    if conn:
        return ('alert',
            TITLE.format(conn['source']),
            BODY.format(conn['user'], conn['process'], conn['pid'], conn['target']),
        )
    return (None, '', '')
