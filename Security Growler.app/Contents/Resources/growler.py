#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Nick Sweeting (nikisweeting) 2014
# MIT Liscense

import os, sys, time, re, itertools, logging
logging.basicConfig(filename='/tmp/securitygrowler-errors.log', level=logging.ERROR)

polling_rate = 3    # number of seconds to wait between re-checking logfiles, increase this number for lower cpu use but slower notifications

def log(text, location="/tmp/securitygrowler-events.log"):
    if log_to_file:
        with open(location, 'a') as so:
            so.write(text+"\n")
    else:
        print(text)

notification_types = ['secnotify', 'secalert']

# tries growl v2
# if no growl v2:
#    tries osx notifications
#    if not osx >=10.8:
#       tries legacy growl
#       if no growl:
#           fallback to silent logging

def get_notifiers():
    try:
        # Try to use Growl version >= 2.0 for notifications
        import gntp, gntp.notifier
        growl = gntp.notifier.GrowlNotifier(applicationName="Security Growler", notifications=notification_types, defaultNotifications=notification_types)
        if not growl.register():
            raise Exception("No Growl >2.0v found.")

        def notify(content="", title="Security Notification", icon='http://i.imgur.com/auYfC7O.png'):
            if content:
                growl.notify(noteType="secnotify", title=title, description=content, icon=icon, sticky=False, priority=1)
                log("[>] secnotify[%s]: %s" % (title, content))
        def alert(content="", title="SECURITY ALERT", icon='http://i.imgur.com/auYfC7O.png'):
            if content:
                growl.notify(noteType="secalert", title=title, description=content, icon=icon, sticky=False, priority=2)
                log("[>] secalert[%s]: %s" % (title, content))

        log("[√] Using Growl version >= 2.0")
        notify(content="Using Growl for security notifications.", title="Security-Growler")

        return notify, alert

    except Exception as e1:
        try:
            # Try OS X Notification Center
            from Foundation import NSUserNotification, NSUserNotificationCenter

            def notify(content="", title="Security Notification", icon=None, sound=None):
                if content:
                    log("[>] secnotify[%s]: %s" % (title, content))
                    notification = NSUserNotification.alloc().init()
                    notification.setTitle_(title)
                    notification.setInformativeText_(content)
                    center = NSUserNotificationCenter.defaultUserNotificationCenter()
                    center.deliverNotification_(notification)
            def alert(content="", title="SECURITY ALERT", icon=None, sound=None):
                if content:
                    log("[>] secalert[%s]: %s" % (title, content))
                    notification = NSUserNotification.alloc().init()
                    notification.setTitle_(title)
                    notification.setInformativeText_(content)
                    center = NSUserNotificationCenter.defaultUserNotificationCenter()
                    center.deliverNotification_(notification)

            log("[√] Using OS X Notification Center (growl not installed: %s)" % e1)
            log("[i] If you prefer Growl, install python-growl by running:\n       `easy_install install gntp`      for Growl version >=2.0\n       `easy_install install appscript` for Growl version <=1.3")
            notify(content="Using OS X Notifcation Center for security notifications.", title="Security-Growler")

            return notify, alert

        except Exception as e2:
            try:
                # Try legacy growl (growl version <1.3)
                # appscript is advertised as import * safe
                from appscript import app
                growl = app('GrowlHelperApp')
                growl.register(as_application='Security Growler', all_notifications=notification_types, default_notifications=notification_types, icon_of_application='/Applications/Utilities/Network Utility.app"')

                def notify(content="", title="Security Notification", icon=False):
                    if content:
                        if icon:
                            growl.notify(with_name='secnotify', title=title, description=content, application_name='Security Growler', image_from_location=icon)
                        else:
                            growl.notify(with_name='secnotify', title=title, description=content, application_name='Security Growler', icon_of_application="/Applications/Utilities/Network Utility.app")
                        log("[>] secnotify[%s]: %s" % (title, content))
                def alert(content="", title="SECURITY ALERT", icon=False):
                    if content:
                        if icon:
                            growl.notify(with_name='secalert', title=title, description=content, application_name='Security Growler', image_from_location=icon)
                        else:
                            growl.notify(with_name='secalert', title=title, description=content, application_name='Security Growler', icon_of_application="/Applications/Utilities/Network Utility.app")
                        log("[>] secalert[%s]: %s" % (title, content))

                log("[√] Detected Growl version <= 1.3")
                notify(content="Using legacy growl.", title="Security-Growler")

                return notify, alert

            except Exception as e3:
                # Fall back to silent logging, no notifications
                log("[X] No available notifcation medium availabe:")
                log("    tried Growl version >2.0: %s" % e1)
                log("    tried OSX Notification Center: %s" % e2)
                log("    tried Growl version >1.3: %s" % e3)
                log("[!] Growl and/or Growl-python support not installed, and OS X notifications not available (OS X >10.8 only).")
                log("[i] If you want to use Growl, run:\n       `easy_install install gntp`      for Growl version >=2.0\n       `easy_install install appscript` for Growl version <=1.3")

                def notify(content="", title="Security Notification", icon=False):
                    pass
                def alert(content="", title="SECURITY ALERT", icon=False):
                    pass

                return notify, alert

def parse(line="", log_type=None):
    # return tuple of event name and details ("event", "line") or ("", "") if nothing parsed
    if not line.strip():
        return ("","")
    if log_type == "secure":
        if "sshd[" in line:
            return ("SSH Connection", line.strip())
        elif "sudo" in line:
            s = line.split("sudo")
            s = ''.join(s[1:])
            s = s.replace(";","\n")
            return ("SUDO Event", s.strip())
    elif log_type == "apache":
        try:
            return "[%s]: %s" % (str(re.search(r'((2[0-5]|1[0-9]|[0-9])?[0-9]\.){3}((2[0-5]|1[0-9]|[0-9])?[0-9])', line, re.I).group()), line.strip())
        except Exception:
            return ("Apache Error Served", line.strip())

    elif log_type == "ftp":
        if "ftpd[" in line:
            return ("FTP Being Accessed", line.strip())
    return ("","")

dead_log = open(r'/dev/null', 'r')

def main():
    notify, alert = get_notifiers()
    notify("Started Security Growler.")
    log("[i]  Watched sources: \n       secure.log (ssh, sudo events)\n       access_log (pages served by webserver)\n       ftp.log (ftp connections)\n       lsof -i :5900 (VNC connctions)")


    if os.path.isfile('/var/log/secure.log'):
        secure_log = open(r'/var/log/secure.log', 'r')
    elif os.path.isfile('/var/log/system.log'):
        secure_log = open(r'/var/log/system.log', 'r')
    else:
        secure_log = dead_log

    ftp_log = open(r'/var/log/ftp.log', 'r') if os.path.isfile('/var/log/ftp.log') else dead_log
    apache_log = open(r'/var/log/apache2/error_log', 'r') if os.path.isfile('/var/log/ftp.log') else dead_log

    while secure_log.readline().strip(): pass
    while apache_log.readline().strip(): pass
    while ftp_log.readline().strip(): pass

    last_vnc_status = ""
    for counter in itertools.cycle([1,2,3]):
        secure_event, secure_line = parse(line=secure_log.readline().strip(), log_type="secure")
        apache_event, apache_line = parse(line=apache_log.readline().strip(), log_type="apache")
        ftp_event, ftp_line = parse(line=ftp_log.readline().strip(), log_type="ftp")

        if (counter % 3 == 0):
            # for cpu intensive tasks, only run checks every third time we check logfiles
            vnc_status = os.popen("lsof -i :5900 | tail -n +2").read().strip()
            if vnc_status != last_vnc_status:
                log("[>] secalert[VNC]: " + vnc_status)
                notify(vnc_status, title="VNC")
            last_vnc_status = vnc_status

        if not (secure_event or apache_event or ftp_event):
            time.sleep(polling_rate)
        else:
            if secure_event:
                log("[>] secnotify[%s]: %s" % (secure_event, secure_line))
                notify(content=secure_line, title=secure_event)
            ### Comment these 2 lines out to disable apache error notifications {
            if apache_event:
                log("[>] secnotify[%s]: %s" % (apache_event, apache_line))
                notify(content=apache_line, title=apache_event)
            ### }
            if ftp_event:
                log("[>] secnotify[%s]: %s" % (ftp_event, ftp_line))
                notify(ftp_line, title=ftp_event)

if __name__ == "__main__":
    log_to_file = True
    try:
        main()
    except Exception as e:
        # generally not advised to catch all exceptions, however it is done here to write the exception to the logfile so that app doesnt fail silently
        # the logfile is displayed by the menubar, where the user will be able to see the [X] EXIT line showing that the secnotify failed and how it failed
        alert(content=e, title="SECURITY GROWLER STOPPED")
        log("[X] EXIT: %s" % e)
        raise e

# TODO: add more logs to watch:
# diff:secure.log: SSH, AFP, VNC, others
#       Jul 31 18:34:18 plato sshd[57985]: Accepted publickey for nick from ::1 port 58410 ssh2
#       Jul 31 18:34:39 plato sshd[57990]: Received disconnect from ::1: 11: disconnected by user
#       Jul 30 15:04:45 plato sudo[22945]:     nick : 1 incorrect password attempt ;
# diff:appfirewall.log
# diff:ftp.log
# change in open ports diff:`sudo lsof -i | grep "(LISTEN)"`
# vnc watch:`sudo lsof -i :5900`
# ssh watch:`sudo lsof -i :22`
