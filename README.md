[Security Growler](http://nikisweeting.github.io/security-growler)
========
This menubar app for OS X will notify you via Growl or Notifcation Center if any SSH, FTP, VNC, AFP, or Sudo authentication events occur.  It's very useful if you're paranoid about people trying to hack into your computer.  Or... if you simply like having information about people using your computer's resources.  It's easily extensible in python, you can add modules that watch logfiles or processes and do whatever you want.

## Install:
1. Download and run [Security Growler.app](https://github.com/nikisweeting/security-growler/raw/master/Security-Growler.app.zip)
2. Run `sudo easy_install gntp` in Terminal to enable Growl support  
 (otherwise events are logged silently to the menubar)


## Information:  
  
I was tired of not being able to find an app that would quell my paranoia about open ports, so I made one myself.  Now I can relax whenever I'm in a seedy internet cafe or connected to free Boingo airport wifi because I know if anyone is trying to connect to my computer.

This app will notify you if any SSH, FTP, VNC, AFP, or sudo authentication events occur.  It also notifies you whenever a page an apache error occurs (although you may want to turn this off if you develop locally, getting growl bubbles on every pageload is annoying).  Simply comment out these three lines in `Security Growler.app/Contents/Resources/growler.py` to do so:  


  ```
  #if apache_event:
  #    print("[>] secnotify[%s]: %s" % (apache_event, apache_line))
  #    notify(content=apache_line, title=apache_event)
  ```
  
====
**Nick Sweeting 2014 -- MIT License**  
