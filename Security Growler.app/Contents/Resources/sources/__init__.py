from time import sleep

from settings import WATCHED_SOURCES, POLLING_SPEED

from sources.logfile import gen_lines
from sources.sockets import gen_conns

all_source_generators = {
    # generator depends on whether source is a port number or file path
    source: gen_conns(source) if type(source) == int else gen_lines(source)
    for source in WATCHED_SOURCES.keys()
}

def get_new_lines(source_generators=all_source_generators, delay=POLLING_SPEED):
    """infinite runloop which reads lines out of their source generators"""

    while True:
        for source, generator in source_generators.iteritems():
            next_line = next(generator)
            while next_line:
                yield (source, next_line)
                next_line = next(generator)
        sleep(delay)
