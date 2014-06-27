#!/bin/sh

SERVICE="growler.py"

if ps ax | grep -v grep | grep $SERVICE > /dev/null
then
    echo "Security Growler is running. 🍺"
    cat /tmp/securitygrowler-events.log
else
    echo "Security Growler is not running. ☹"
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    rm /tmp/securitygrowler*
    python "$DIR"/growler.py > /tmp/securitygrowler-sh.log 2>&1 &
fi
