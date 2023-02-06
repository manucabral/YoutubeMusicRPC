import time
import os
from .presence import Presence
from .logger import Logger
from .tab import Tab
from .utils import remote_debugging, run_browser, get_default_browser, get_browser_tabs


class App:
    """Core class of the application."""

    __slots__ = (
        "__presence",
        "__browser",
        "last_tab",
        "connected",
        "version",
        "title",
    )

    def __init__(
        self,
        client_id: str = None,
        version: str = None,
        title: str = None,
    ):
        os.system("title " + title + " v" + version)
        Logger.write(message=f"{title} v{version}", level="INFO", origin=self)
        Logger.write(message="initialized.", origin=self)
        self.__presence = Presence(client_id=client_id)
        self.version = version
        self.title = title
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
            Logger.write(message=f"{self.__browser['fullname']} detected.", origin=self)
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
                Logger.write(
                    message=f"Playing {self.last_tab.title} by {self.last_tab.artist}",
                    origin=self,
                )
                state = self.last_tab.artist
                self.__presence.update(
                    details=self.last_tab.title,
                    state=state,
                    large_image="logo",
                    large_text=f"{self.title} v{self.version}",
                    small_image="pause" if self.last_tab.pause else "play",
                    small_text=self.__browser["fullname"],
                    buttons=[
                        {"label": "Play", "url": self.last_tab.url},
                        {
                            "label": "Download App",
                            "url": "https://manucabral.github.io/YoutubeMusicRPC/",
                        },
                    ],
                    start=time.time(),
                )
                time.sleep(15)
        except Exception as exc:
            self.__handle_exception(exc)
            if exc.__class__.__name__ == "URLError":
                Logger.write(
                    message="Please close all browser instances and try again. Also, close Youtube Music Desktop App if you are using it.",
                    level="WARN",
                    origin=self,
                )
