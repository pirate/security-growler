import re

# Apr 20 03:30:11 squash kernel[0]: Limiting closed port RST response from 382 to 250 packets per second
PORTSCAN_EVENT_FILTER = re.compile('kernel\[\d+\]: Limiting closed port RST response')

def parse(line, source=None):
    if PORTSCAN_EVENT_FILTER.findall(line):
        return ('alert',
            'Incoming Portscan Detected',
            'Limiting ' + line.split('port RST response ', 1)[-1])
    return (None, '', '')
