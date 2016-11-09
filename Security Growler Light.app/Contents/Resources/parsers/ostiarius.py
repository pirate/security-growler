import re

# 27/04/16 09:42:38,000 kernel[0]: OSTIARIUS: /Applications/Xoib.app/Contents/MacOS/Xoib is from the internet & is unsigned -> BLOCKING!
OSTIARIUS_EVENT_FILTER = re.compile('OSTIARIUS: .+BLOCKING')

def parse(line, source=None):
    if OSTIARIUS_EVENT_FILTER.findall(line):
        return ('alert', 'Ostiarius', line.split('OSTIARIUS: ', 1)[-1])
    return (None, '', '')
