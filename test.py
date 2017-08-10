import threading
import subprocess

COMMAND = ['log', 'stream', '--style', 'syslog', '--predicate', 'process == "sshd"', '--info']


class SSHMonitor(object):
    def __init__(self):
        self.proc = subprocess.Popen(COMMAND, stdout=subprocess.PIPE, bufsize=1)

    def poll(self):
        return self.proc.stdout.read(1)



if __name__ == '__main__':
    monitors = [SSHMonitor()]


    print('[+] Starting growler')

    while True:
        alerts = []
        for mon in monitors:
            alerts += mon.poll()

        if alerts:
            print '[!] %s' % alerts
        else:
            print '.',
