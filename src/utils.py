# Yep, it's the magic utils file. It's not made to be pretty.

import re
import json
import subprocess as sp
import urllib.request as req
from .browsers import BROWSERS
from .tab import Tab

ENDPOINT = "http://127.0.0.1:9222/json"


def request(url: str) -> bytes:
    with req.urlopen(url) as response:
        return response.read()


def remote_debugging() -> bool:
    try:
        request(ENDPOINT)
        return True
    except Exception:
        return False


def find_browser(key: str, value: str) -> dict | None:
    for browser in BROWSERS:
        if re.search(browser[key], value, re.IGNORECASE):
            return browser
    return None


def find_browser_by_process(os_string: str, target_process: str) -> dict | None:
    for browser in BROWSERS:
        if re.search(browser["process"][os_string], target_process, re.IGNORECASE):
            return browser
    return None




def get_browser_tabs(filter_url: str = "") -> list:
    tabs = request(ENDPOINT).decode("utf-8")
    tabs = json.loads(tabs)
    tabs = [tab for tab in tabs if filter_url in tab["url"] and tab["type"] == "page"]
    return tabs


def run_browser(browser_executable_path: str,
                profile_directory:str,
                user_directory:str
                ) -> None:
    sp.Popen(
        [
            browser_executable_path,
            "--profile-directory=" + profile_directory,
            "--user-data-dir" + user_directory,
            "--remote-debugging-port=9222",
            "--remote-allow-origins=http://127.0.0.1:9222"
        ]
    )


def current_playing_tab(tabs: Tab) -> dict:
    tabs = get_browser_tabs(filter_url="music.youtube.com")
    if tabs:
        for tab_data in tabs:
            tab = Tab(**tab_data)
            tab.update()
            if tab.playing:
                return tab
    return None
