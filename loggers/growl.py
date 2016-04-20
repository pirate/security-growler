"""Logger that outputs notifications to growl"""

from time import sleep

try:
    import gntp
    import gntp.notifier  # must be imported separately
except ImportError:
    raise Exception('Please `pip install gntp` if you want to use Growl.')

from settings import (
    APP_NAME,
    NOTIFICATION_TYPES,

    INFO_TYPE,
    INFO_ICON,
    INFO_TITLE,
    INFO_STICKY,
    INFO_PRIORITY,

    ALERT_TYPE,
    ALERT_ICON,
    ALERT_TITLE,
    ALERT_STICKY,
    ALERT_PRIORITY,
)

# Register the app with growl and check that it works
GROWL = gntp.notifier.GrowlNotifier(
    applicationName=APP_NAME,
    notifications=NOTIFICATION_TYPES,
    defaultNotifications=NOTIFICATION_TYPES,
)
try:
    success = GROWL.register()
except gntp.errors.NetworkError:
    success = True

if not success:
    raise Exception("gntp installed but no Growl app (>2.0v) found.")


### Exported functions for use in the app
def notify(content, title=INFO_TITLE, icon=INFO_ICON):
    if not content: return

    try:
        GROWL.notify(
            noteType=INFO_TYPE,
            title=title,
            description=content,
            icon=icon,
            sticky=INFO_STICKY,
            priority=INFO_PRIORITY,
        )
    except gntp.errors.NetworkError:
        pass


def alert(content, title=ALERT_TITLE, icon=ALERT_ICON):
    if not content: return

    try:
        GROWL.notify(
            noteType=ALERT_TYPE,
            title=title,
            description=content,
            icon=icon,
            sticky=ALERT_STICKY,
            priority=ALERT_PRIORITY,
        )
    except gntp.errors.NetworkError:
        pass
