"""Logger that outputs notifications to OS X Notification Center"""

try:
    from Foundation import NSUserNotification, NSUserNotificationCenter
except ImportError:
    raise Exception('You must be on OS X 10.8 or above to use Notification Center')

import datetime

from settings import (
    INFO_TITLE,
    INFO_SOUND,
    ALERT_TITLE,
    ALERT_SOUND,
)

def timestamp():
    return datetime.datetime.now().strftime('%H:%M')

NOTIFICATION_CENTER = NSUserNotificationCenter.defaultUserNotificationCenter()

### Exported functions for use in the app
def notify(content, title=INFO_TITLE, icon=None, sound=INFO_SOUND):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_('{0} @ {1}'.format(title, timestamp()))
    notification.setInformativeText_(content)
    if sound:
        notification.setSoundName_('NSUserNotificationDefaultSoundName')
    NOTIFICATION_CENTER.deliverNotification_(notification)

def alert(content, title=ALERT_TITLE, icon=None, sound=ALERT_SOUND):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_('{0} @ {1}'.format(title, timestamp()))
    notification.setInformativeText_(content)
    if sound:
        notification.setSoundName_('NSUserNotificationDefaultSoundName')
    NOTIFICATION_CENTER.deliverNotification_(notification)
