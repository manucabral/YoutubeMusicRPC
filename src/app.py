import time
from .presence import Presence
from .logger import Logger
from .tab import Tab
from .utils import remote_debugging, run_browser, get_default_browser, get_browser_tabs


class App:
    """Core class of the application."""

    __slots__ = ("__presence", "last_tab", "connected", "__browser")

    def __init__(self, client_id: str = None):
        Logger.write(message="initialized.", origin=self)
        self.__presence = Presence(client_id=client_id)
        self.last_tab = None
        self.connected = False
        self.__browser = None

    def __handle_exception(self, exc: Exception) -> None:
        Logger.write(message=exc, level="ERROR", origin=self)

    def sync(self) -> None:
        Logger.write(message="syncing..", origin=self)
        try:
            self.__presence.connect()
            self.__browser = get_default_browser()
            if not self.__browser:
                raise Exception("Can't find default browser.")
            if not self.__browser["chromium"]:
                raise Exception("Unsupported browser, sorry.")
            self.connected = True
            Logger.write(message="synced and connected.", origin=self)
        except Exception as exc:
            self.__handle_exception(exc)

    def stop(self) -> None:
        self.connected = False
        self.__presence.close()
        Logger.write(message="stopped.", origin=self)

    def update_tabs(self) -> None:
        tabs = []
        tab_list = get_browser_tabs(filter_url="music.youtube.com")
        if tab_list:
            for tab_data in tab_list:
                tab = Tab(**tab_data)
                tab.update()
                tabs.append(tab)
        return tabs

    def current_playing_tab(self, tabs: list) -> dict:
        if tabs:
            for tab in tabs:
                if tab.playing:
                    return tab
            for tab in tabs:
                if tab.pause:
                    return tab
        return None

    def run(self) -> None:
        Logger.write(message="running.", origin=self)
        try:
            if not self.connected:
                raise RuntimeError("Not connected.")
            if not remote_debugging():
                Logger.write(
                    message="Remote debugging is not enabled.",
                    level="WARNING",
                    origin=self,
                )
                Logger.write(message="Starting browser remote debugging..", origin=self)
                run_browser(self.__browser)
            while self.connected:
                tabs = self.update_tabs()
                tab = [tab for tab in tabs if tab.playing] or [
                    tab for tab in tabs if tab.pause
                ]
                if not tab:
                    continue
                tab = tab[0]
                if self.last_tab == tab:
                    continue
                self.last_tab = tab
                print(self.last_tab.title, self.last_tab.artist, self.last_tab.album)
                state = self.last_tab.artist
                if self.last_tab.pause:
                    state += " (Paused)"
                self.__presence.update(
                    details=self.last_tab.title,
                    state=state,
                    large_image="logo",
                    buttons=[{"label": "Play", "url": self.last_tab.url}],
                    start=time.time(),
                )
                time.sleep(15)
        except Exception as exc:
            raise exc
            self.__handle_exception(exc)
