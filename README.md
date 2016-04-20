[Security Growler](http://pirate.github.io/security-growler)
========
This menubar app for OS X will notify you via Growl or Notifcation Center if any SSH, FTP, VNC, AFP, or Sudo authentication events occur.  It's very useful if you're paranoid about people trying to hack into your computer.  Or... if you simply like having information about people using your computer's resources.  It's easily extensible in python, you can add modules that watch logfiles or processes and do whatever you want.  You can even send them as push notiifcations to your iOS device using [Prowl](http://prowlapp.com/).

## Install:
1. Download and run [Security Growler.app](https://github.com/nikisweeting/security-growler/raw/master/Security-Growler.app.zip)
2. Click on the menubar icon once to start detecting events

Optionally, run `sudo easy_install gntp` in Terminal to enable Growl support (otherwise it defaults to using OS X Notification Center).

![](http://pirate.github.io/security-growler/screenshots/menubar_1.PNG)
![](http://pirate.github.io/security-growler/screenshots/menubar_2.PNG)

### It can do cool things like:

**Let you know when you're being portscanned:**

![](http://pirate.github.io/security-growler/screenshots/portscan_context.PNG)
![](http://pirate.github.io/security-growler/screenshots/portscan_event.PNG)

**Alert you to attempted and succesfull SSH logins:**

![](http://pirate.github.io/security-growler/screenshots/ssh_fail_event.PNG)
![](http://pirate.github.io/security-growler/screenshots/ssh_key_event.PNG)

**Notify you whenever a command is run with sudo:**

![](http://pirate.github.io/security-growler/screenshots/sudo_context.PNG)
![](http://pirate.github.io/security-growler/screenshots/sudo_event.PNG)

**Notify you of arbitrary TCP connections: VNC, PostgreSQL, even plain HTTP:**

![](http://pirate.github.io/security-growler/screenshots/vnc_event.PNG)
![](http://pirate.github.io/security-growler/screenshots/connection_event.PNG)

![](http://pirate.github.io/security-growler/screenshots/menubar_3.PNG)

----

## Information:

I was tired of not being able to find an app that would quell my paranoia about open ports, so I made one myself. Now I can relax whenever I'm in a seedy internet cafe or connected to free Boingo airport wifi because I know if anyone is trying to connect to my computer.

This app will notify you if any SSH, FTP, VNC, AFP, or Sudo auth events occur.

It does **not** increase your security in any way, it just notifies you **who** and **when** people are authenticated on your computer. It also notifies you whenever an apache error occurs (although you may want to turn this off if you develop locally, getting growl bubbles on every pageload is annoying).

A related project is available for Linux users: [PushAlotAuth](https://github.com/benjojo/PushAlotAuth), it uses the PushALot push-notification platform.

## Developer Info:

The menubar app is a simple wrapper for the python script, compiled using [Platypus](http://www.macupdate.com/app/mac/12046/platypus).  `Security Growler-dev.app` is symlinked to run `growler.py` for development.  `Security Growler.app` is packaged and uses it's prebuilt `growler.py`.  To make changes to the app, change `menubar.sh`, and `growler.py`, and run `Security Growler-dev.app` to test your changes.  Once you're done, submit a pull request.

The menubar app works by simply running `growler.py` (which writes to a log file), then `cat`ing the contents of `/tmp/securitygrowlerevents.log` and displaying them in the dropdown.  See `menubar.sh` for more details.



## License:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, pulverize, distribute, synergize, compost, defenestrate, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

If the Author of the Software (the "Author") needs a place to crash and you have a sofa available, you should maybe give the Author a break and let him sleep on your couch.

If you are caught in a dire situation wherein you only have enough time to save one person out of a group, and the Author is a member of that group, you must save the Author.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO BLAH BLAH BLAH ISN'T IT FUNNY HOW UPPER-CASE MAKES IT SOUND LIKE THE LICENSE IS ANGRY AND SHOUTING AT YOU.
