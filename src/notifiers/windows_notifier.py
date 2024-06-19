import os
from .toast_notifier import ToastNotifier
from .notifier import Notifier

class WindowsNotifier(Notifier):
    def __init__(self):
        self.toast = ToastNotifier()

    def notify(self, title: str, subtitle: str) -> None:
        assets_path = os.path.join(os.getcwd(), 'assets')
        notifier_path = os.path.join(assets_path, 'notifier')
        icon_path = os.path.join(notifier_path, 'icon.ico')
        self.toast.show_toast(
            title,
            subtitle,
            duration = 3,
            icon_path = icon_path,#os.path.join(os.getcwd(), 'icon.ico'),
            threaded = True,
        )
