#!/bin/bash

SERVICE=growler.py
OUTFILE=~/SecurityGrowler.log

if ps ax | grep -v grep | grep $SERVICE > /dev/null
then
    # Growler is already running, display its output
    echo "🍺 Security Growler is running."
    echo "======================================="
    tail -50 $OUTFILE
    echo "======================================="
    echo "View the full log at $OUTFILE"
else
    DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    rm $OUTFILE
    echo "               🍺      Starting...      🍺"
    echo ""
    echo " information:  pirate.github.io/security-growler"
    echo " support:      github.com/pirate/security-growler/issues"
    echo " my website:   nicksweeting.com"
    # echo " twitter:      @thesquashSH"

    # run Growler in the background and save its output to OUTFILE
    python "$DIR"/"$SERVICE" 2>&1>> $OUTFILE &
fi
