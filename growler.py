# -*- coding: utf-8 -*-
# MIT Liscence

import os, sys, time, re
from appscript import *
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler



# TODO: logs to watch:
# apache2: access_log
# secure.log: SSH, AFP, VNC, others
#       Jul 31 18:34:18 plato sshd[57985]: Accepted publickey for nick from ::1 port 58410 ssh2
#       Jul 31 18:34:39 plato sshd[57990]: Received disconnect from ::1: 11: disconnected by user
#       Jul 30 15:04:45 plato sudo[22945]:     nick : 1 incorrect password attempt ; 
# appfirewall.log
# ftp.log
# prey.log
#        == Sending report!
# nmap
#       change in open ports
# vnc watchdog "lsof -i :5900"
# ssh watchdog "lsof -i :22"

polling_rate = 2

# connect to Growl
growl = app('GrowlHelperApp')
allNotificationsList = ['secnotify', 'secalert']
enabledNotificationsList = ['secnotify', 'secalert']
growl.register(as_application='Security Growler', all_notifications=allNotificationsList, default_notifications=enabledNotificationsList, icon_of_application='NanoStudio.app')

def growlnotify(content="", title="Security Notification", icon="NanoStudio.app"):
    growl.notify(with_name='secnotify', title=title, description=content, application_name='Security Growler', icon_of_application=icon)
    print "[>] secnotify[%s]: %s" % (title, content)

def growlalert(content="", title="SECURITY ALERT", icon="Network Utility.app"):
    growl.notify(with_name='secalert', title=title, description=content, application_name='Security Growler', icon_of_application=icon)
    print "[>] secalert[%s]: %s" % (title, content)

def parse(line="", log_type=None):

    if log_type == "secure":
        if line.find("sshd[") != -1:
            return line
        elif line.find("sudo") != -1 and line.find("failed") != -1:
            return line

    elif log_type == "apache":
        if line.find("GET") != -1:
            ip = re.search(r'((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9])', line, re.I).group()
            return ip
            
    elif log_type == "ftp":
        if line.find("ftpd[") != -1:
            return line
    else:
        return line

if __name__=="__main__":
    try:
        exit = 0
        first_run = True
        print("[+] Starting Security Growl Notifier.")
        growlnotify("Started Security Growler")
    
        secure = open(r'/var/log/secure.log', 'r')
        ftp = open(r'/var/log/ftp.log', 'r')
        apache = open(r'/var/log/apache2/access_log', 'r')
    
        while not exit:
            secure_line = secure.readline()
            apache_line = apache.readline()
            ftp_line = ftp.readline()
    
            if not (secure_line or apache_line or ftp_line):
                first_run = False
                time.sleep(polling_rate)
            else:
                if not first_run:
                    if secure_line: growlnotify(secure_line.strip())
                    if apache_line: growlnotify(apache_line.strip())
                    if ftp_line: growlnotify(ftp_line.strip())
    
    except KeyboardInterrupt:
        print("[X] EXIT.")
    except Exception as e:
        print("[X] EXIT: %s" % e)
    sys.exit(0)