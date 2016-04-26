import re

FTP_EVENT_FILTER = re.compile('ftpd\[\d+\]')

def parse(line, source=None):
    if FTP_EVENT_FILTER.findall(line):
        return ('notify', 'FTP Access', line.split('ftpd', 1)[-1])
    return (None, '', '')
