# -*- coding: utf-8 -*-
# MIT Liscense

import os, sys, time, re

### Remove/comment this block to disable logging stdout/err to a file
filename="/tmp/securitygrowlerevents.log" 
so = se = open(filename, 'w', 0)
# re-open stdout without buffering
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
# redirect stdout and stderr to the log file
os.dup2(so.fileno(), sys.stdout.fileno())
os.dup2(se.fileno(), sys.stderr.fileno())
### Endblock

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

polling_rate = 3
allNotificationsList = ['secnotify', 'secalert']

try:
    try:
        from appscript import *
        growl = app('GrowlHelperApp')
        growl.register(as_application='Security Growler', all_notifications=allNotificationsList, default_notifications=allNotificationsList, icon='http://i.imgur.com/auYfC7O.png"')
        def growlnotify(content="", title="Security Notification", icon="/Applications/Utilities/Network Utility.app"):
            if content:
                growl.notify(with_name='secnotify', title=title, description=content, application_name='Security Growler', icon_of_application=icon)
                print "[>] secnotify[%s]: %s" % (title, content)
    
        def growlalert(content="", title="SECURITY ALERT", icon="/Applications/Utilities/Network Utility.app"):
            if content:
                growl.notify(with_name='secalert', title=title, description=content, application_name='Security Growler', icon_of_application=icon)
                print "[>] secalert[%s]: %s" % (title, content)
        print "[i] Detected Growl version <= 1.3"
    
    except ApplicationNotFoundError:
        import gntp
        import gntp.notifier
        growl = gntp.notifier.GrowlNotifier(applicationName = "Security Growler", notifications = allNotificationsList, defaultNotifications = allNotificationsList)
        growl.register()
        def growlnotify(content="", title="Security Notification", icon="http://i.imgur.com/auYfC7O.png"):
            if content:
                growl.notify(noteType="secnotify", title=title, description=content, icon=icon, sticky=False, priority=1)
                print "[>] secnotify[%s]: %s" % (title, content)
    
        def growlalert(content="", title="SECURITY ALERT", icon="http://i.imgur.com/auYfC7O.png"):
            if content:
                growl.notify(noteType="secalert", title=title, description=content, icon=icon, sticky=False, priority=1)
                print "[>] secalert[%s]: %s" % (title, content)
        print "[i] Detected Growl version >= 2.0"
except Exception as e:
    print "[X] Error initializing: %s" % e
    print "[!] Growl support not installed, install it using:\n       `easy_install install gntp`      for Growl version >=2.0\n       `easy_install install appscript` for Growl version <=1.3"
    def growlnotify(content="", title="Security Notification"):
        if content:
            print "[>] secnotify[%s]: %s" % (title, content)
    def growlalert(content="", title="SECURITY ALERT", ):
        if content:
            print "[>] secalert[%s]: %s" % (title, content)

def parse(line="", log_type=None):
    if log_type == "secure":
        if line.find("sshd[") != -1:
            return line.strip()
        elif line.find("sudo") != -1 and line.find("failed") != -1:
            return line.strip()
        else:
            return ""

    elif log_type == "apache":
        if line.find("GET") != -1:
            try:
                ip = re.search(r'((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9])', line, re.I).group()
                return ip
            except:
                return line.strip()
        else:
            return ""

    elif log_type == "ftp":
        if line.find("ftpd[") != -1:
            return line.strip()
        else:
            return ""
    else:
        return line

if __name__=="__main__":
    try:
        exit = 0
        first_run = True
        counter = 0
        last_vnc_status = ""

        print("[+] Starting Security Growl Notifier.")
        print("[i]  Watched sources: \n       secure.log (ssh, sudo events)\n       access_log (pages served by webserver)\n       ftp.log (ftp connections)\n       lsof -i :5900 (VNC connctions)")
        growlnotify("Started Security Growler.")
     
        secure = open(r'/var/log/secure.log', 'r')
        ftp = open(r'/var/log/ftp.log', 'r')
        apache = open(r'/var/log/apache2/access_log', 'r')

        while not exit:
            secure_line = secure.readline().strip()
            apache_line = apache.readline().strip()
            ftp_line = ftp.readline().strip()
    
            if not (secure_line or apache_line or ftp_line):
                first_run = False
                time.sleep(polling_rate)
            else:
                if not first_run:
                    if secure_line: 
                        secure_line = parse(line=secure_line, log_type="secure")
                        growlnotify(content=secure_line, title="SSH & Sudo")
                    if apache_line: 
                        apache_line = parse(line=apache_line, log_type="apache")
                        growlnotify(content=apache_line, title="Apache2 Webserver")
                    if ftp_line: 
                        ftp_line = parse(line=ftp_line, log_type="ftp")
                        growlnotify(ftp_line, title="FTP")

            if (counter % 3 == 0):
                vnc_status = os.popen("lsof -i :5900 | tail -n +2").read().strip()
                if vnc_status != last_vnc_status:
                    growlnotify(vnc_status, title="VNC")
                last_vnc_status = vnc_status
            elif counter > 3000:
                counter = 0
                #to prevent rollover (i think python protects against rollover by allocated memory but im just being safe)
            counter += 1
    
    except KeyboardInterrupt:
        print("[X] EXIT.")
    except Exception as e:
        print("[X] EXIT: %s" % e)
    raise SystemExit(0)
