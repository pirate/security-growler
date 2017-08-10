"""Detect changes in a logfile"""

# files = {path for path in paths if os.path.isfile(path)}

def gen_lines(path):
    """generator which yields new lines from a logfile, or None"""
    with open(path, 'r') as logfile:
        logfile.seek(0, 2)  # jump to end
        yield 'ready'       # otherwise it will hang until the first change appears
        while True:
            yield logfile.readline().strip() or None
