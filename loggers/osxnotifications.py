NAME = "Notification Center"

try:
    from Foundation import NSUserNotification, NSUserNotificationCenter
except ImportError:
    raise Exception('You must be on OS X 10.8 or above to use Notification Center')

import datetime


def alert(title, body, level='INFO', time=None):
    time = (time or datetime.datetime.now()).strftime('%H:%M')

    if level == 'WARNING':
        warn(title=title, body=body, time=time)
    else:
        info(title=title, body=body, time=time)



NOTIFICATION_CENTER = NSUserNotificationCenter.defaultUserNotificationCenter()

def info(title, body, time, sound=False):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_('{0} @ {1}'.format(title, time))
    notification.setInformativeText_(body)
    if sound:
        notification.setSoundName_('NSUserNotificationDefaultSoundName')
    NOTIFICATION_CENTER.deliverNotification_(notification)

def warn(title, body, time, sound=False):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_('{0} @ {1}'.format(title, time))
    notification.setInformativeText_(body)
    if sound:
        notification.setSoundName_('NSUserNotificationDefaultSoundName')
    NOTIFICATION_CENTER.deliverNotification_(notification)
