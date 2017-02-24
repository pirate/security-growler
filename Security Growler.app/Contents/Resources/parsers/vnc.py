from .connections import parse_connection

TITLE = 'VNC CONNECTED {source}'
BODY = 'To: {user} {process} ({pid}) on {target}'

def parse(line, source=None):
    conn = parse_connection(line, source)
    if conn:
        return ('alert',
            TITLE.format(**conn),
            BODY.format(**conn),
        )
    return (None, '', '')
