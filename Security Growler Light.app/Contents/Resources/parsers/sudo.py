import re

# Apr 19 23:41:33 squash sudo[3620]:   squash : TTY=ttys001 ; PWD=/Users/squash ; USER=root ; COMMAND=/usr/bin/whoami

SUDO_EVENT_FILTER = re.compile('sudo')

TITLE = 'SUDO EVENT: {0} [{1}]'
BODY = '{0}\n@ {1}'

def parse(line, source=None):
    if SUDO_EVENT_FILTER.findall(line) and '/usr/sbin/lsof +c 0' not in line:
        pre, pwd, _, command = line.split(' ; ', 3)

        user = pre.split(' : ', 1)[0].split(' ')[-1]
        tty = pre.split('TTY=', 1)[-1].strip()
        command = command.split('COMMAND=', 1)[-1]
        pwd = pwd.split('PWD=', 1)[-1].split('/Users/', 1)[-1]

        return ('alert',
            TITLE.format(user, tty),
            BODY.format(command, pwd))

    return (None, '', '')
