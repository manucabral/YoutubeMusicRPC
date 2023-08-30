import time
import os
import math
from .presence import Presence
from .logger import Logger
from .tab import Tab
from .utils import (
    remote_debugging,
    run_browser,
    get_default_browser,
    get_browser_tabs,
    find_windows_process,
)

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
        "__profileName",
        "refreshRate",
        "useTimeLeft",
    )

    def __init__(
        self,
        client_id: str = "",
        version: str = None,
        title: str = None,
        profileName: str = "Default",
        refreshRate: int = 1,
        useTimeLeft: str = "yes",
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
        self.refreshRate = refreshRate
        self.useTimeLeft = useTimeLeft
        self.__profileName = profileName

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
        global lastUpdated
        global compareTab
        compareTab = {"title": "", "artist": "", "artwork": "", "lastTime": 0}
        lastUpdated = 1
        try:
            if not self.connected:
                raise RuntimeError("Not connected.")
            browser_process = self.__browser["process"]["win32"]
            browser_running = find_windows_process(
                browser_process, self.__browser["name"]
            )
            if not remote_debugging() and browser_running:
                Logger.write(
                    message=f"Detected browser running ({browser_process}) without remote debugging enabled.",
                    level="WARNING",
                    origin=self,
                )
                raise RuntimeError("Please close all browser instances and try again.")
            if not remote_debugging():
                Logger.write(
                    message="Remote debugging is not enabled, starting browser..",
                    level="WARNING",
                    origin=self,
                )
                run_browser(self.__browser, self.__profileName)
            else:
                Logger.write(
                    message="Remote debugging is enabled, connected successfully.",
                    origin=self,
                )
            Logger.write(message="synced and connected.", origin=self)
            Logger.write(message="Starting presence loop..", origin=self)
            time.sleep(3)
            while self.connected:
                # time.sleep(self.refreshRate)
                tabs = self.update_tabs()
                tab = [tab for tab in tabs if tab.playing] or [
                    tab for tab in tabs if tab.pause
                ]
                if not tab:
                    Logger.write(message="No tab found.", origin=self)
                    self.__presence.update(
                        details="No activity",
                        large_image="logo",
                        small_image="pause",
                        small_text=self.__browser["fullname"],
                        buttons=[
                            {
                                "label": "Download App",
                                "url": "https://manucabral.github.io/YoutubeMusicRPC/",
                            },
                        ],
                    )
                    time.sleep(DISCORD_STATUS_LIMIT)
                    continue
                tab = tab[0]
                compareTab["title"] = tab.title
                compareTab["artwork"] = tab.artwork
                compareTab["artist"] = tab.artist
                compareTab["lastTime"] = tab.start
                if tab.ad:
                    Logger.write(message="Ad detected.", origin=self)
                    time.sleep(DISCORD_STATUS_LIMIT)
                    continue
                if self.last_tab == tab:
                    # fixed problem where it didn't detect the page change (appears to happen sometimes in playlists)
                    if (
                        compareTab["title"] == self.last_tab.title
                        and compareTab["artist"] == self.last_tab.artist
                    ):
                        time.sleep(self.refreshRate)
                        continue
                if self.last_tab:
                    if (
                        compareTab["title"] == self.last_tab.title
                        and compareTab["artist"] == self.last_tab.artist
                    ):
                        time.sleep(self.refreshRate)
                        continue
                    if self.last_tab.start == compareTab["lastTime"]:
                        time.sleep(self.refreshRate)
                        continue

                if lastUpdated + 15 > time.time():
                    remaining = time.time() - (lastUpdated + 15)
                    if remaining < 0:
                        remaining = 1
                    time.sleep(remaining)
                    continue
                lastUpdated = time.time()
                self.last_tab = tab
                Logger.write(
                    message=f"Playing {self.last_tab.title} by {self.last_tab.artist}",
                    origin=self,
                )

                def useTimeLeft(answer):
                    if answer == "yes":
                        return self.last_tab.end + self.refreshRate
                    return None

                self.__presence.update(
                    details=self.last_tab.title,
                    state=self.last_tab.artist,
                    large_image=self.last_tab.artwork,
                    large_text=f"{self.title} v{self.version}",
                    small_image="pause" if self.last_tab.pause else "play",
                    small_text=self.__browser["fullname"],
                    buttons=[
                        {"label": "Listen In Youtube Music", "url": self.last_tab.url},
                        {
                            "label": "Download App",
                            "url": "https://manucabral.github.io/YoutubeMusicRPC/",
                        },
                    ],
                    # TODO: enhance time left -> Done! --Nelly
                    start=self.last_tab.start,
                    end=useTimeLeft(self.useTimeLeft),
                )
                # time.sleep(self.refreshRate)
        except Exception as exc:
            self.__handle_exception(exc)
            if exc.__class__.__name__ == "URLError":
                Logger.write(
                    message="Please close all browser instances and try again. Also, close Youtube Music Desktop App if you are using it.",
                    level="WARN",
                    origin=self,
                )
