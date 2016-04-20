[Security Growler](http://pirate.github.io/security-growler)
========

<img src="http://pirate.github.io/security-growler/screenshots/portscan_event.PNG" width="40%"/>
<img src="http://pirate.github.io/security-growler/screenshots/vnc_event.PNG" width="40%"/>

This menubar app for OS X will notify you via Notifcation Center (or Growl) when various system security events occur (full list of supported events below).

It's very useful if you're paranoid about people trying to hack into your computer.  Or... if you simply like having information about people using your computer's resources.

It's easily extensible in python, you can add modules that watch ports for connetions or parse logfiles.  You can even forward alerts as push notiifcations to your iOS device using [Prowl](http://prowlapp.com/).

## Install:
1. Download and run [Security Growler.app](https://github.com/nikisweeting/security-growler/raw/master/Security-Growler.app.zip)
2. Click on the menubar icon once to start detecting events.

Optionally, run `sudo easy_install gntp` in Terminal to enable Growl support (otherwise it defaults to using OS X Notification Center).

<img src="http://pirate.github.io/security-growler/screenshots/menubar_1.PNG" width="45%" margin-bottom="300px"/>
<img src="http://pirate.github.io/security-growler/screenshots/menubar_2.PNG" width="45%"/>

## It can do cool things like:

**Alert you to attempted and succesfull SSH logins:**

<img src="http://pirate.github.io/security-growler/screenshots/ssh_fail_event.PNG" width="40%"/>
<img src="http://pirate.github.io/security-growler/screenshots/ssh_key_event.PNG" width="40%"/>

**Notify you of arbitrary TCP connections: VNC, PostgreSQL, even plain HTTP:**

<img src="http://pirate.github.io/security-growler/screenshots/vnc_event.PNG" width="40%"/>
<img src="http://pirate.github.io/security-growler/screenshots/connection_event.PNG" width="40%"/>

**Notify you whenever a command is run with sudo:**

<!-- ![](http://pirate.github.io/security-growler/screenshots/sudo_event.PNG) -->
<img src="http://pirate.github.io/security-growler/screenshots/sudo_context.PNG" height="400px"/>

**Let you know when you're being portscanned:**

<img src="http://pirate.github.io/security-growler/screenshots/portscan_context.PNG" height="400px"/>

[More Screenshots...](https://github.com/pirate/security-growler/tree/gh-pages/screenshots)

----

## Information:

I was tired of not being able to find an app that would quell my paranoia about open ports, so I made one myself. Now I can relax whenever I'm in a seedy internet cafe or connected to free Boingo airport wifi because I know if anyone is trying to connect to my computer.

The currently working notifiers are:

    * SSH
    * FTP
    * SMB
    * AFP
    * VNC
    * MySQL
    * PostgreSQL
    * iTunes Sharing
    * sudo commands
    * port-scans (e.g. if you're on the receiving end of nmap)

Feel free to submit a pull-request and add a new one (e.g. try writing one for http-auth)!

A related project is available for Linux users: [PushAlotAuth](https://github.com/benjojo/PushAlotAuth), it uses the PushALot push-notification platform.

## Developer Info:

This app is composed of 3 main parts: sources, parsers, and loggers.

 * `sources` are either file paths or port numbers, e.g. `/var/log/system.log` or `5900`
 * `parsers` take the text from the `sources`, and parse out various alerts, e.g. `ssh` or `sudo`
 * `loggers` are output channels for alerts, e.g. `stdout`, `osxnotifications`, or `growl`

The main runloop is in `growler.py`, it reads lines out of the sources, passes them through parsers, then dispatches alerts before waiting a short delay and then looping.

The menubar app is a simple wrapper compiled using [Platypus](http://www.macupdate.com/app/mac/12046/platypus).  `Security Growler.app` is packaged with copies of `growler.py` and all the other files it needs.
To make changes to the app, change the files you need, test using `sudo python growler.py` and `sudo ./menubar.sh`, then re-run Platypus to generate a new app.

The menubar app works by simply running `growler.py` (which writes to a log file), then `cat`ing the contents of the logfile to show in the dropdown.
See `menubar.sh` for more details.


## License:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, pulverize, distribute, synergize, compost, defenestrate, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

If the Author of the Software (the "Author") needs a place to crash and you have a sofa available, you should maybe give the Author a break and let him sleep on your couch.

If you are caught in a dire situation wherein you only have enough time to save one person out of a group, and the Author is a member of that group, you must save the Author.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO BLAH BLAH BLAH ISN'T IT FUNNY HOW UPPER-CASE MAKES IT SOUND LIKE THE LICENSE IS ANGRY AND SHOUTING AT YOU.



<img src="http://pirate.github.io/security-growler/screenshots/menubar_3.PNG" width="100%"/>
