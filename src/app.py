import time
import os
from .presence import Presence
from .logger import Logger
from .notifiers.notifier import Notifier
from .system_tray.system_tray import SystemTray
from .tab import Tab
from .operating_systems.operating_system import OperatingSystem
from .utils import (
    remote_debugging,
    get_browser_tabs,
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
        "showen",
        "systray",
        "silent",
        "__operating_system",
        "notifier",
    )

    def __init__(
        self,
        operating_system: OperatingSystem,
        notifier: Notifier,
        systray: SystemTray = None,
        client_id: str = "",
        version: str = None,
        title: str = None,
        profileName: str = "Default",
        refreshRate: int = 1,
        useTimeLeft: bool = True,
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
        self.showen = True
        self.refreshRate = refreshRate
        self.useTimeLeft = useTimeLeft
        self.silent = False
        self.__profileName = profileName
        self.__operating_system = operating_system
        self.notifier = notifier
        self.systray = systray

    def __handle_exception(self, exc: Exception) -> None:
        Logger.write(message=exc, level="ERROR", origin=self)

    def sync(self) -> None:
        Logger.write(message="syncing..", origin=self)
        try:
            status = self.__presence.connect()
            if not status:
                raise Exception("Can't connect to Discord.")
            self.__browser = self.__operating_system.get_default_browser()
            if not self.__browser:
                raise Exception("Can't find default browser in your system.")
            if not self.__browser["chromium"]:
                raise Exception("You have an unsupported browser.")
            self.connected = True
            Logger.write(message=f"{self.__browser['fullname']} detected.", origin=self)
        except Exception as exc:
            #raise exc
            self.__handle_exception(exc)

    def stop(self) -> None:
        if self.connected == True:
            self.connected = False
            self.systray.stop()
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

    def on_quit_callback(self, systray):
        if self.connected == True:
            self.connected = False
            self.__presence.close()
            Logger.write(message="stopped.", origin=self)

    def run(self) -> None:
        last_updated_time: int = 1
        try:
            if not self.connected:
                raise RuntimeError("Not connected.")
            browser_running = self.__operating_system.is_browser_running()
            if not remote_debugging() and browser_running:
                Logger.write(
                    message=f"Detected browser running ({self.__operating_system.get_browser_process_name()}) without remote debugging enabled.",
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
                self.__operating_system.run_browser_with_debugging_server(self.__profileName)
            else:
                Logger.write(
                    message="Remote debugging is enabled, connected successfully.",
                    origin=self,
                )
            Logger.write(message="synced and connected.", origin=self)
            Logger.write(message="Starting presence loop..", origin=self)
            time.sleep(3)
            while self.connected:
                self.silent = False
                update_unix_time: float = time.time()
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
                if tab.ad:
                    Logger.write(message="Ad detected.", origin=self)
                    time.sleep(DISCORD_STATUS_LIMIT)
                    continue

                if self.last_tab and self.last_tab == tab:
                    # fixed problem where it didn't detect the page change (appears to happen sometimes in playlists)
                    delta_estimated_end_times = abs(self.last_tab.projected_end_time - tab.projected_end_time)
                    playstate_manually_adjusted = delta_estimated_end_times > 1 
                    self.silent = self.last_tab.projected_end_time + self.refreshRate < update_unix_time or playstate_manually_adjusted
                    if (
                        tab.title == self.last_tab.title
                        and tab.artist == self.last_tab.artist
                        and tab.projected_end_time + self.refreshRate > update_unix_time
                        and not playstate_manually_adjusted
                        and not tab.pause
                    ):
                        time.sleep(self.refreshRate)
                        continue

                if tab.pause:
                    self.silent = True

                if self.last_tab and self.last_tab.start_time == tab.start_time:
                    time.sleep(self.refreshRate)
                    continue

                if last_updated_time + 15 > update_unix_time:
                    remaining = update_unix_time - (last_updated_time + 15)
                    if remaining < 0:
                        remaining = 1
                    time.sleep(remaining)
                    continue
                last_updated_time = update_unix_time
                self.last_tab = tab

                Logger.write(
                    message=f"Playing {self.last_tab.title} by {self.last_tab.artist}",
                    origin=self,
                    silent=self.silent
                )
                
                if not self.silent and self.notifier is not None:
                    try:
                        self.notifier.notify("Now Playing!",
                                             f"{self.last_tab.title} by {self.last_tab.artist}"
                                            )
                    except TypeError:
                        pass
                
                self.__presence.update(
                    silent=self.silent,
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
                    start=self.last_tab.start_time,
                    end=self.last_tab.projected_end_time + self.refreshRate if self.useTimeLeft else None
                )
                # time.sleep(self.refreshRate)
        except Exception as exc:
            self.__handle_exception(exc)
            # raise exc
            if exc.__class__.__name__ == "URLError":
                Logger.write(
                    message="Please close all browser instances and try again. Also, close Youtube Music Desktop App if you are using it.",
                    level="WARN",
                    origin=self,
                )