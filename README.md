**Nick Sweeting 2013 -- MIT License**  
Security Growler
========
This app will notify you if any SSH, FTP, VNC, AFP, or sudo authentication events occur.  
It's mostly userful if you're paranoid about people trying to hack into your computer.

## Install:
1. Download and run [Security Growler.app](https://github.com/nikisweeting/security-growler/raw/master/Security-Growler.app.zip)
2. Run `sudo easy_install gntp` in Terminal to enable Growl support (otherwise events are logged silently to the menubar)


## Information:  
  
I was tired of not being able to find an app that would quell my paranoia about open ports, so I made one myself.  Now I can relax whenever I'm in a seedy internet cafe or connected to free Boingo airport wifi because I know if anyone is trying to connect to my computer.

This app will notify you if any SSH, FTP, VNC, AFP, or sudo authentication events occur.  It also notifies you whenever a page is served by apache (althouh you may want to turn this off if you develop using it, getting a growl bubble on every pageload is annoying).  Simply comment out these three lines in `Security Growler.app/Contents/Resources/growler.py` to do so:  


  ```
  if apache_line:
      apache_line = parse(line=apache_line, log_type="apache")
      growlnotify(content=apache_line, title="Apache2 Webserver")
  ```
  
This project was started in August 2013, and is so far only being worked on by me.
If you want to help, fork and send a pull request, or email me.
    
   
===