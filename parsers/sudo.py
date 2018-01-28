import re
from sys import platform as _platform
if _platform == "Darwin":
    pwd_split = '/Users/'
else:
    pwd_split = '/home/'

# Apr 19 23:41:33 squash sudo[3620]:   squash : TTY=ttys001 ; PWD=/Users/squash ; USER=root ; COMMAND=/usr/bin/whoami

SUDO_EVENT_FILTER = re.compile('sudo')

TITLE = 'SUDO EVENT: {user} [{tty}]'
BODY = '{command}\n@ {pwd}'

EXCLUDE_LINES = ('/usr/sbin/lsof +c 0',)  # dont alert on sudo events that contain these strings


def parse(line, source=None):
    if SUDO_EVENT_FILTER.findall(line) and 'COMMAND' in line and not any(pattern in line for pattern in EXCLUDE_LINES) :
        pre, pwd, _, command = line.split(' ; ', 3)

        user = pre.split(' : ', 1)[0].split(' ')[-1]
        tty = pre.split('TTY=', 1)[-1].strip()
        command = command.split('COMMAND=', 1)[-1]
        pwd = pwd.split('PWD=', 1)[-1].split(pwd_split, 1)[-1]

        return ('alert',
            TITLE.format(user=user, tty=tty),
            BODY.format(command=command, pwd=pwd))

    return (None, '', '')
