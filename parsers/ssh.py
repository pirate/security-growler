import re

# Apr 20 00:05:01 squash sshd[58113]: Accepted keyboard-interactive/pam for squash from fe80::82e6:50ff:fe16:b2dc%en0 port 54978 ssh2
PASSWORD_EVENT_FILTER = re.compile('sshd(\[\d+\])?: Accepted (keyboard|password)')

# Apr 19 23:42:17 squash sshd[10906]: Accepted publickey for root from ::1 port 54336 ssh2: RSA SHA256:ZzsSwM7Qcrk/QkE2pSJj8Bkb7L91bp3deUpo0wQ9uBg
KEYAUTH_EVENT_FILTER = re.compile('sshd\[\d+\]: Accepted publickey for ')

# Apr 20 00:27:16 squash sshd[88153]: error: PAM: authentication error for squash from fe80::82e6:50ff:fe16:b2dc%en0 via fe80::82e6:50ff:fe16:b2dc%en0
# Apr 20 00:57:47 squash sshd[40882]: Postponed keyboard-interactive for squash from 192.168.2.52 port 56316 ssh2 [preauth]
# Apr 20 02:45:25 squash sshd[68819]: Connection closed by fe80::82e6:50ff:fe16:b2dc%en0 [preauth]
FAIL_EVENT_FILTER = re.compile(' sshd\[\d+\]: ')


def word_after(line, word):
    """'a black sheep', 'black' -> 'sheep'"""
    return line.split(word, 1)[-1].split(' ', 1)[0]

def parse_summary(line):
    """get the summary of an SSH failure from an SSH log event line"""
    return line.split(' sshd[', 1)[-1].split(' ', 1)[-1][:40] + '...'

def parse_line(line):
    """parse out the user and connection source from an SSH log event line"""
    user = (
        word_after(line, ' for ')
        if ' for ' in line else ' '
    )
    src = (
        word_after(line, ' from ')
        if ' from ' in line else
        (word_after(line, ' by ') if ' by 'in line else '')
    )
    return user, src


def parse(line, source=None):
    """parse SSHD event log lines into pass and fail alerts messages"""
    title, body = '', ''

    if KEYAUTH_EVENT_FILTER.findall(line) or PASSWORD_EVENT_FILTER.findall(line):
        user, src = parse_line(line)
        title = 'SSH LOGIN SUCCESS: %s' % user
        method = 'Password' if ' keyboard' or ' password' in line else 'Public Key'
        body = 'from: %s using a %s' % (src, method)


    elif FAIL_EVENT_FILTER.findall(line):
        user, src = parse_line(line)
        summary = parse_summary(line)
        title = 'SSH EVENT: %s' % user or (summary[:15] + '...')
        body = 'from: %s | %s' % (src, summary)

    return ('alert' if title else None, title, body)
