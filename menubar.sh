#!/bin/bash

OS=$(uname -s)
SERVICE=growler.py
OUTFILE=/tmp/SecurityGrowler.log
case $OS in
    Darwin)
        OUTFILE=~/Library/Logs/SecurityGrowler.log
        ;;
    Linux)
        mkdir ~/.logs &>/dev/null
        OUTFILE=~/.logs/SecurityGrowler.log
        ;;
esac
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

Open() {
    case $OS in
        Darwin)
            open $@
            ;;
        Linux)
            xdg-open $@
            ;;
    esac
}

# Menu-item actions
[[ $1 == "Settings..."* || $1 == *" Started Watching Sources"* || $1 == "port "* ]] &&
    Open "$DIR"/settings.py

[[ $1 == "View the full log..."* ]] &&
    Open $OUTFILE

[[ $1 == "Clear"* ]] &&
    echo `date +"[%m/%d %H:%M]"` "--------" >> $OUTFILE

[[ $1 == "Stop the background agent"* ]] &&
    echo `date +"[%m/%d %H:%M]"` "Stopped." >> $OUTFILE &&
    kill `ps aux | grep 'growler\.py' | awk '{print $2}'` &&
    kill `ps aux | grep 'Security Growler\.app' | awk '{print $2}'` &&
    exit 0

[[ $1 == " my website: "* ]] &&
    Open 'https://nicksweeting.com'

[[ $1 == *"@thesquashSH"* ]] &&
    Open 'https://twitter.com/thesquashSH'

[[ $1 == " information: "* || $1 == "About Security Growler" ]] &&
    Open 'https://pirate.github.io/security-growler/'

[[ $1 == " support: "* || $1 == "Request a Feature" ]] &&
    Open 'https://github.com/pirate/security-growler/issues'

# Helpful logfile line actions
[[ $1 == *" VNC "* || $1 == *" PORT "* ]] &&
    Open '/System/Library/PreferencePanes/SharingPref.prefPane'

[[ $1 == *" SUDO "* ]] &&
    Open '/Applications/Utilities/Activity Monitor.app'

[[ $1 == "/var/log/"* ]] &&
    Open /var/log/


# Growler is already running, display its output
if ps ax | grep -v grep | grep $SERVICE > /dev/null
then
    echo "Settings..."
    echo "Clear menubar log"
    echo "View the full log..."
    echo "—————————————————————————————————————————————————————————"
    sed -n 'H; / --------$/h; ${g;p;}' $OUTFILE | tail +2 | tail -30
    echo "—————————————————————————————————————————————————————————"
    echo "Request a Feature"
    echo "About Security Growler"
    echo "Stop the background agent & Quit"

# Otherwise start it and display the loading output
else
    echo `date +"[%m/%d %H:%M]"` "--------" >> $OUTFILE
    echo "               🍺      Starting...      🍺"
    echo " "
    echo " information:  pirate.github.io/security-growler"
    echo " support:      github.com/pirate/security-growler/issues"
    echo " my website:   nicksweeting.com"
    echo " "
    echo "   🍀   Tweet @thesquashSH if you like this app!    🍀  "

    # run Growler in the background and save its output to OUTFILE
    python2 "$DIR"/"$SERVICE" 2>&1>> $OUTFILE &
fi

sleep 0.1  # small delay to allow menubar to buffer text before rendering
