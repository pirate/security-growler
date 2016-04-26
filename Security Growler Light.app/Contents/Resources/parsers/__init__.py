from settings import WATCHED_SOURCES

from parsers import default

PARSERS = {}
for source, parsers in WATCHED_SOURCES.items():
    parsers = [parsers] if type(parsers) == str else parsers
    parser_modules = []
    for module_name in parsers:
        if module_name:
            try:
                exec('from parsers import %s' % module_name)
                parser_modules.append(eval('%s' % module_name))
            except ImportError:
                print('[X] Parser module not found! %s' % module_name)
        else:
            parser_modules.append(default)

    PARSERS[source] = tuple(parser_modules)

def get_sources_info():
    """/var/log/system.log      : for sudo,auth events
       port 5900                : for vnc events
       port 22                  : for ssh events
    """
    return '\n'.join(
        '{0}: {1}'.format(
            ('port %s' % source if type(source) == int else source).ljust(25),
            'for %s events' % ','.join(
                f.__name__.split('.', 1)[-1]  # parsers.ssh -> ssh
                for f in parsers
            )
        )
        for source, parsers in PARSERS.items()
    )

def parse_line(line, source=None):
    for parser in PARSERS[source]:
        alert_type, title, content = parser.parse(line, source)
        if alert_type:
            return (alert_type, title, content)

    return (None, '', '')
