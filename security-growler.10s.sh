#!/bin/bash
#
# <bitbar.title>Security Growler</bitbar.title>
# <bitbar.version>v3.6</bitbar.version>
# <bitbar.author>Nick Sweeting</bitbar.author>
# <bitbar.author.github>pirate</bitbar.author.github>
# <bitbar.desc>See pirate.github.io/security-growler</bitbar.desc>
# <bitbar.dependencies>security growler</bitbar.dependencies>

export PATH="/usr/local/bin:/usr/bin:$PATH"


growler_bin=~/Documents/Code/security-growler/growler.py
OUTFILE=~/Library/Logs/SecurityGrowler.log




pid=$(ps ax | grep -v grep | grep growler\.py | awk '{print $1}')


if [[ $pid ]]; then

# Agent is Running
echo "📡 ‼️ | color=red"
echo "---"
echo "✓ Notifications On | bash=/usr/bin/true terminal=false"
echo "𐄂  Menubar Summary Off | bash=/usr/bin/true terminal=false"
echo "---"
echo "Recent Events"
tail -8 "$OUTFILE" | replace "|" "" | uniq   # replace | to mitigate bitbar "xss"
echo "See full log... | bash=/usr/bin/open param1=$OUTFILE terminal=false"
echo "---"

else

# Agent is stopped
echo "🛰"
echo "---"
echo "Monitoring is off"
[[ $pid ]] || echo "Start Monitoring ↠ | bash=python param1=\"$growler_bin\" terminal=false"
echo "---"
echo "See full log... | bash=/usr/bin/open param1=$OUTFILE terminal=false"

fi



echo "Toggle Events to Monitor"
echo "-- Sudo | color=#33ff33 bash=/usr/bin/say param1=on terminal=false"
echo "-- SSH | color=#33ff33 bash=/usr/bin/say param1=on terminal=false"
echo "-- VNC (off) | color=#ff3333 bash=/usr/bin/say param1=on terminal=false"
echo "-- FTP (off) | color=#ff3333 bash=/usr/bin/say param1=on terminal=false"
echo "-- SMB (on) | color=#33ff33 bash=/usr/bin/say param1=on terminal=false"
echo "-- AFP (on) | color=#33ff33 bash=/usr/bin/say param1=on terminal=false"
echo "-- iTunes Sharing (on) | color=#33ff33 bash=/usr/bin/say param1=on terminal=false"
echo "-- MySQL | color=#33ff33 bash=/usr/bin/say param1=on terminal=false"
echo "-- PostgreSQL | color=#33ff33 bash=/usr/bin/say param1=on terminal=false"
echo "-- portscans | color=#33ff33 bash=/usr/bin/say param1=on terminal=false"
echo "-- ostiarius | color=#33ff33 bash=/usr/bin/say param1=on terminal=false"
echo "-- Add new monitor... | bash=/usr/bin/open param1=on terminal=false"

echo "---"
echo ":computer: About..."
echo "-- Website & Docs | href=http://pirate.github.io/security-growler"
echo "-- Check for Updates | href=https://github.com/pirate/security-growler/releases"
echo "-- 🍺 Donate if you like it | href=https://twitter.com/thesquashSH"
echo "-- 🍀 Tweet @thesquashSH | href=https://twitter.com/thesquashSH"

[[ $pid ]] && echo "⚙ Advanced Settings | bash=/usr/bin/open param1=~/.security-growler.conf terminal=false"
[[ $pid ]] && echo ":red_circle: Stop Monitoring | bash=/bin/bash param1=-c param2=\"kill $pid && kill $$\" terminal=false"

