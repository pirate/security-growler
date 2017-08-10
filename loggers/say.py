import subprocess

NAME = "Speak Alerts"

def alert(level, title, body, time=None):
    subprocess.Popen(['say', title])
