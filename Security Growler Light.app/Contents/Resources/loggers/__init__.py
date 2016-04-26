from settings import LOGGERS

for logger in LOGGERS:
    exec('from loggers import %s' % logger)

enabled_loggers = [eval('%s' % module) for module in LOGGERS]

def notify(*args, **kwargs):
    for logger in enabled_loggers:
        logger.notify(*args, **kwargs)

def alert(*args, **kwargs):
    for logger in enabled_loggers:
        logger.alert(*args, **kwargs)
