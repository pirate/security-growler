TITLE = 'PORT {port} <- {source}'
BODY = '{user} {process} ({pid}) @ {target}'

def parse_connection(log_line, port=None):
    details = log_line.split()[:10]
    try:
        proc, pid, user, _, tcp_vers, _, _, _, addrs, state = details
    except ValueError:
        return None
    addrs = addrs.split('->')
    target, src = addrs if len(addrs) == 2 else [addrs[0], '*']

    return {
        'tcp_version': tcp_vers,
        'port': port or '',
        'state': state[1:-1],  # removes parens (LISTEN) -> LISTEN
        'user': user,
        'process': str(proc),
        'pid': pid,
        'source': src,
        'target': target,
    }


def parse(line, source=None):
    conn = parse_connection(line, source)
    if conn:
        return ('notify',
            TITLE.format(**conn),
            BODY.format(**conn))

    return (None, '', '')
