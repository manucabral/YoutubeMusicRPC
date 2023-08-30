# Yep, it's the magic utils file. It's not made to be pretty.

import re
import json
import winreg as wr
import os
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


def find_browser(progid) -> dict:
    for browser in BROWSERS:
        if re.search(browser["name"], progid, re.IGNORECASE):
            return browser
    return None


def find_windows_process(process_name: str, ref: str) -> bool:
    res = sp.check_output(
        "WMIC PROCESS WHERE \"name='{process_name}'\" GET ExecutablePath",
        stderr=sp.PIPE,
    ).decode()
    return bool(re.search(ref, res))


def get_default_browser() -> dict:
    progid = wr.QueryValueEx(
        wr.OpenKey(
            wr.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice",
        ),
        "ProgId",
    )[0]
    if not progid:
        raise Exception("Can't find default browser")
    browser = find_browser(progid.split(".")[0])
    if not browser:
        raise Exception("Unsupported browser, sorry")
    browser["path"] = wr.QueryValueEx(
        wr.OpenKey(wr.HKEY_CLASSES_ROOT, progid + "\shell\open\command"), ""
    )[0].split('"')[1]
    return browser


def get_browser_tabs(filter_url: str = "") -> list:
    tabs = request(ENDPOINT).decode("utf-8")
    tabs = json.loads(tabs)
    tabs = [tab for tab in tabs if filter_url in tab["url"] and tab["type"] == "page"]
    return tabs


def run_browser(browser: dict, profileDirec) -> None:
    # profileDirec ="Profile 1"
    profilePath = f'{os.environ["SYSTEMDRIVE"]}\\Users\\{os.getenv("USERNAME") + browser["profilePath"] + profileDirec}'
    sp.Popen(
        [
            browser["path"],
            "--profile-directory=" + profileDirec,
            "--user-data-dir" + profilePath,
            "--app-id=cinhimbnkkaeohfgghhklpknlkffjgod",
            "--remote-debugging-port=9222",
            "--remote-allow-origins=*",
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
