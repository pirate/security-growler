"""Logger that outputs notifications to OS X or Gnome Notification Center"""

import datetime
try:
    import gi
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
    from gi.repository import GLib
    Notify.init("Security Growler")
except ImportError:
    raise Exception('You need the `libnotify` and `python-gobject` libraries')

from settings import (
    INFO_TITLE,
    INFO_SOUND,
    ALERT_TITLE,
    ALERT_SOUND,
)

def timestamp():
    return datetime.datetime.now().strftime('%H:%M')

### Exported functions for use in the app
def notify(content, title=INFO_TITLE, icon=None, sound=INFO_SOUND):
    notification = Notify.Notification.new(
        '{0} @ {1}'.format(title, timestamp()),
        content,
        "dialog-information"
    )
    notification.set_urgency(Notify.Urgency.NORMAL)
    # notification.set_hint("sound-file", GLib.Variant.new_string(sound))
    notification.show()

def alert(content, title=ALERT_TITLE, icon=None, sound=ALERT_SOUND):
    notification = Notify.Notification.new(
        '{0} @ {1}'.format(title, timestamp()),
        content,
        "dialog-information"
    )
    notification.set_urgency(Notify.Urgency.CRITICAL)
    # notification.set_hint("sound-file", GLib.Variant.new_string(sound))
    notification.show()
