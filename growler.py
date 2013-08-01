# -*- coding: utf-8 -*-
# MIT Liscence

import sys
from appscript import *

# connect to Growl
growl = app('GrowlHelperApp')

# Make a list of all the notification types 
# that this script will ever send:
allNotificationsList = ['secnotify', 'secalert']

# Make a list of the notifications 
# that will be enabled by default.      
# Those not enabled by default can be enabled later 
# in the 'Applications' tab of the growl prefpane.
enabledNotificationsList = ['secnotify', 'secalert']

# Register our script with growl.
# You can optionally (as here) set a default icon 
# for this script's notifications.
growl.register(as_application='Security Growler', all_notifications=allNotificationsList, default_notifications=enabledNotificationsList, icon_of_application='NanoStudio.app')

def growlnotify(content="", title="Security Notification", icon="NanoStudio.app"):
	growl.notify(with_name='secnotify', title=title, description=content, application_name='Security Growler', icon_of_application=icon)
	print "secnotify[%s]: %s" % (title, content)

def growlalert(content="", title="SECURITY ALERT", icon="Network Utility.app"):
	growl.notify(with_name='secalert', title=title, description=content, application_name='Security Growler', icon_of_application=icon)
	print "secalert[%s]: %s" % (title, content)

growlnotify("hi how are you")
growlalert("you suck balls")

print("[X] EXIT.")
sys.exit(0)