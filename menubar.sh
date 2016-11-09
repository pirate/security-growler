#!/bin/bash

SERVICE=growler.py
OUTFILE=~/Library/Logs/SecurityGrowler.log
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Menu-item actions
[[ $1 == "Settings..."* || $1 == *" Started Watching Sources"* || $1 == "port "* ]] &&
    open "$DIR"/settings.py

[[ $1 == "Check for updates" ]] &&
    open "https://github.com/pirate/security-growler/releases"

# once sc auto-starts on launch instead of requiring a click on the menu icon
# [[ $1 == "Start Security Growler at login" ]] &&
    # defaults write loginwindow AutoLaunchedApplicationDictionary -array-add '{ "Path" = "/Applications/Security Growler.app"; "Hide" = 0; }'

[[ $1 == "View the full log..."* ]] &&
    open $OUTFILE

[[ $1 == "Clear"* ]] &&
    echo `date +"[%m/%d %H:%M]"` "--------" >> $OUTFILE

[[ $1 == "Stop the background agent"* ]] &&
    echo `date +"[%m/%d %H:%M]"` "Stopped." >> $OUTFILE &&
    kill `ps aux | grep 'growler\.py' | awk '{print $2}'` &&
    kill `ps aux | grep 'Security Growler' | awk '{print $2}'` &&
    exit 0

[[ $1 == " my website: "* ]] &&
    open 'https://nicksweeting.com'

[[ $1 == *"@thesquashSH"* ]] &&
    open 'https://twitter.com/thesquashSH'

[[ $1 == " information: "* || $1 == "About Security Growler" ]] &&
    open 'https://pirate.github.io/security-growler/'

[[ $1 == " support: "* || $1 == "Request a feature" ]] &&
    open 'https://github.com/pirate/security-growler/issues'

# Helpful logfile line actions
[[ $1 == *" VNC "* || $1 == *" PORT "* ]] &&
    open '/System/Library/PreferencePanes/SharingPref.prefPane'

[[ $1 == *" SUDO "* ]] &&
    open '/Applications/Utilities/Activity Monitor.app'

[[ $1 == "/var/log/"* ]] &&
    open /var/log/


# Growler is already running, display its output
if ps ax | grep -v grep | grep $SERVICE > /dev/null
then
    echo "Settings..."
    echo "Clear menubar log"
    echo "View the full log..."
    echo "—————————————————————————————————————————————————————————"
    sed -n 'H; / --------$/h; ${g;p;}' $OUTFILE | tail +2 | tail -30
    echo "—————————————————————————————————————————————————————————"
    echo "Check for updates"
    echo "Request a feature"
    echo "About Security Growler"
    # echo "Start Security Growler at login"
    echo "Stop the background agent & quit"

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
    python "$DIR"/"$SERVICE" 2>&1>> $OUTFILE &
fi

sleep 0.1  # small delay to allow menubar to buffer text before rendering
