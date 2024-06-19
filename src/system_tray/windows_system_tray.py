from .system_tray import SystemTray
from ..notifiers.toast_notifier import ToastNotifier
from infi.systray import SysTrayIcon
import win32con
import win32gui
import ctypes

class WindowsSystemTray(SystemTray):
    def start(self) -> None:
        menu_options = (("Hide/Show Console", None, self._hide_window), ("Force Update", None, self._update))
        self.systray = SysTrayIcon("./icon.ico", "YT Music RPC", menu_options, on_quit=self.on_quit_callback)
        self.systray.start()
    
    def stop(self) -> None:
        #TODO: ? No idea
        pass

    def _update(self) -> None:
        toast = ToastNotifier()
        try:
            toast.show_toast(
                "Coming soon!",
                "This feature isn't currently avaiable yet.",
                duration = 5,
                icon_path = f"{os.path.join(os.getcwd(), 'icon.ico')}",
                threaded = True,
            )
        except TypeError:
            pass

    def _hide_window(self) -> None:
        if self.showen is True:
            self.showen = False
            window = ctypes.windll.kernel32.GetConsoleWindow()
            win32gui.ShowWindow(window, win32con.SW_HIDE)
        elif self.showen is False:
            self.showen = True
            window = ctypes.windll.kernel32.GetConsoleWindow()
            win32gui.ShowWindow(window, win32con.SW_SHOW)
