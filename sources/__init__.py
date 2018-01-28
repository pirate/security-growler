from time import sleep

from settings import WATCHED_SOURCES, POLLING_SPEED

from sources.logfile import gen_lines
from sources.systemd import gen_lines as gen_journal_lines
from sources.sockets import gen_conns

all_source_generators = {}
for source in WATCHED_SOURCES.keys():
    if type(source) == int:
        all_source_generators[source] = gen_conns(source)
    elif source == 'systemd':
        all_source_generators[source] = gen_journal_lines()
    else:
        gen_lines(source)

def get_new_lines(source_generators=all_source_generators, delay=POLLING_SPEED):
    """infinite runloop which reads lines out of their source generators"""

    while True:
        for source, generator in source_generators.iteritems():
            next_line = next(generator)
            while next_line:
                yield (source, next_line)
                next_line = next(generator)
        sleep(delay)
