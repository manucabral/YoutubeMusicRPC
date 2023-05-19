import time
import os
from .presence import Presence
from .logger import Logger
from .tab import Tab
from .utils import remote_debugging, run_browser, get_default_browser, get_browser_tabs

DISCORD_STATUS_LIMIT = 15


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
        Logger.write(message="initialized, to stop, press CTRL+C.", origin=self)
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
            status = self.__presence.connect()
            if not status:
                raise Exception("Can't connect to Discord.")
            self.__browser = get_default_browser()
            if not self.__browser:
                raise Exception("Can't find default browser in your system.")
            if not self.__browser["chromium"]:
                raise Exception("You have an unsupported browser.")
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
            Logger.write(message="Starting presence loop..", origin=self)
            time.sleep(5)
            while self.connected:
                tabs = self.update_tabs()
                tab = [tab for tab in tabs if tab.playing] or [
                    tab for tab in tabs if tab.pause
                ]
                if not tab:
                    Logger.write(message="No tab found.", origin=self)
                    time.sleep(DISCORD_STATUS_LIMIT)
                    continue
                tab = tab[0]
                if self.last_tab == tab:
                    time.sleep(DISCORD_STATUS_LIMIT)
                    continue
                self.last_tab = tab
                state = self.last_tab.artist if self.last_tab.artist else "Unknown"
                details = self.last_tab.title if self.last_tab.title else "Unknown"
                artwork = self.last_tab.artwork if self.last_tab.artwork else "logo"
                Logger.write(
                    message=f"Playing {state} by {details}",
                    origin=self,
                )
                self.__presence.update(
                    details=details,
                    state=state,
                    large_image=artwork,
                    large_text=f"{self.title} v{self.version}",
                    small_image="pause" if self.last_tab.pause else "play",
                    small_text=self.__browser["fullname"],
                    buttons=[
                        {"label": "Listen to Youtube Music", "url": self.last_tab.url},
                        {
                            "label": "Download App",
                            "url": "https://manucabral.github.io/YoutubeMusicRPC/",
                        },
                    ],
                    start=time.time(),
                )
                time.sleep(DISCORD_STATUS_LIMIT)
        except Exception as exc:
            self.__handle_exception(exc)
            if exc.__class__.__name__ == "URLError":
                Logger.write(
                    message="Please close all browser instances and try again. Also, close Youtube Music Desktop App if you are using it.",
                    level="WARN",
                    origin=self,
                )
