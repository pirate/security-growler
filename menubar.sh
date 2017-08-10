#!/bin/bash
#
# <bitbar.title>Security Growler</bitbar.title>
# <bitbar.version>v3.6</bitbar.version>
# <bitbar.author>Nick Sweeting</bitbar.author>
# <bitbar.author.github>pirate</bitbar.author.github>
# <bitbar.desc>See pirate.github.io/security-growler</bitbar.desc>
# <bitbar.dependencies>security growler</bitbar.dependencies>

export PATH="/usr/local/bin:/usr/bin:/bin$PATH"

[[ -e .running ]] && ON=1 || ON=""

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

LOGGERS="/Users/squash/Documents/Code/security-growler/loggers"
MONITORS="/Users/squash/Documents/Code/security-growler/monitors"

BITBAR_FILE="/Users/squash/Documents/Code/security-growler/menubar.sh"

GROWLER_BIN=/Users/squash/Documents/Code/security-growler/growler.py
OUTFILE=/Users/squash/Library/Logs/SecurityGrowler.log

cd /Users/squash/Documents/Code/security-growler

if test -e $DIR/.running; then

    echo "📡"
    echo "---"
    echo "Monitoring is on | color=green"

    python2.7 $GROWLER_BIN >> $OUTFILE

else
    echo "🛰"
    echo "---"
    echo "Monitoring is off | color=red"
fi

echo "Toggle events to monitor"
for filename in $MONITORS/*.py; do
    base=$(basename "$filename" | replace '.py' '')
    echo "$base" | grep '_.*' > /dev/null && continue
    name=$(grep 'NAME = ' "$filename" | replace 'NAME = ' '' | replace '"' '')
    [[ "$name" ]] || name=$base
    echo "-- ✓ $name | color=#33ff33 | bash=/bin/mv param1=$filename param2=${filename}.disabled terminal=false refresh=true"
done
stat -t $MONITORS/*.py.disabled >/dev/null 2>&1 &&
for filename in $MONITORS/*.py.disabled; do
    base=$(basename "$filename" | replace '.py.disabled' '')
    echo "$base" | grep '_.*' > /dev/null && continue
    name=$(grep 'NAME = ' "$filename" | replace 'NAME = ' '' | replace '"' '')
    [[ "$name" ]] || name=$base
    enabled=$(echo "$filename" | replace '.py.disabled' '.py')
    echo "-- ⅹ $name | color=#ff3333 | bash=/bin/mv param1=$filename param2=$enabled terminal=false refresh=true"
done
echo "-- Add new monitor type... | bash=/usr/bin/open param1=monitors terminal=false"



echo "---"
echo "Recent Events"
tail -8 "$OUTFILE" | replace "|" "" | uniq   # replace | to mitigate bitbar "xss"
echo "View logfile... | bash=/usr/bin/open param1=$OUTFILE terminal=false"
echo "Clear recent events | bash=/bin/bash param1=-c param2=\"'cat $OUTFILE >> ${OUTFILE}.old && echo $(date +"[%H:%M %p]") Cleared > $OUTFILE'\" terminal=false refresh=True"
echo "---"

echo ":speaker: Notifications"
for filename in $LOGGERS/*.py; do
    base=$(basename "$filename" | replace '.py' '')
    echo "$base" | grep '_.*' > /dev/null && continue
    name=$(grep 'NAME = ' "$filename" | replace 'NAME = ' '' | replace '"' '')
    [[ "$name" ]] || name=$base
    echo "-- ✓ $name | color=green | bash=/bin/mv param1=$filename param2=${filename}.disabled terminal=false refresh=true"
done
stat -t $LOGGERS/*.py.disabled >/dev/null 2>&1 &&
for filename in $LOGGERS/*.py.disabled; do
    base=$(basename "$filename" | replace '.py.disabled' '')
    echo "$base" | grep '_.*' > /dev/null && continue
    name=$(grep 'NAME = ' "$filename" | replace 'NAME = ' '' | replace '"' '')
    [[ "$name" ]] || name=$base
    enabled=$(echo "$filename" | replace '.py.disabled' '.py')
    echo "-- ⅹ $name | color=red | bash=/bin/mv param1=$filename param2=$enabled terminal=false refresh=true"
done
echo "-- Add new alert type... | bash=/usr/bin/open param1=loggers terminal=false"


echo ":computer: More info"
echo "-- Website & Docs | href=http://pirate.github.io/security-growler"
echo "-- Check for Updates | href=https://github.com/pirate/security-growler/releases"
echo "-- How to respond to alerts | href=https://github.com/pirate/security-growler#how-should-you-respond-to-alerts"
echo "-- API for writing custom alerts | href=https://github.com/pirate/security-growler#developer-info"
# echo "-- 🍺 Donate if you like it | href=https://twitter.com/thesquashSH"
echo "-- 🍀 Tweet @thesquashSH | href=https://twitter.com/thesquashSH"

echo "📦 View archived logs | bash=/usr/bin/open param1=${OUTFILE}.old param2=-a param3=Console.app terminal=false tooltip=${OUTFILE}.old"
echo "---"
# echo "⚙ View advanced settings | bash=/usr/bin/open param1=~/.security-growler.conf terminal=false"
test -e $DIR/.running && echo "Quit | bash=/bin/rm param1=$DIR/.running terminal=false refresh=true"
test -e $DIR/.running || echo "Start monitoring | color=green bash=/usr/bin/touch param1=$DIR/.running terminal=false refresh=true"

