# source: https://github.com/manucabral/pybrinf/blob/main/pybrinf/browsers.py

BROWSERS = [
    {
        "name": "Chrome",
        "fullname": "Google Chrome",
        "process": {"win32": "chrome.exe", "linux": "google-chrome"},
        "progid": "ChromeHTML",
        "chromium": True,
    },
    {
        "name": "Yandex",
        "fullname": "Yandex Browser",
        "process": {"win32": "browser.exe", "linux": "yandex-browser"},
        "chromium": True,
        "progid": "YandexHTML",
    },
    {
        "name": "Edge",
        "fullname": "Microsoft Edge",
        "process": {"win32": "msedge.exe", "linux": "sure??"},
        "progid": "EdgeHTML",
        "chromium": True,
    },
    {
        "name": "Opera",
        "fullname": "Opera",
        "process": {"win32": "opera.exe", "linux": "..."},
        "progid": "OperaHTML",
        "chromium": True,
    },
    {
        "name": "Opera GXStable",
        "fullname": "Opera GX",
        "process": {"win32": "opera.exe", "linux": "..."},
        "progid": "OperaGXHTML",
        "chromium": True,
    },
    {
        "name": "OperaDev",
        "fullname": "Opera Developer (Opera One)",
        "process": {"win32": "opera.exe", "linux": "..."},
        "progid": "Operadeveloper",
        "chromium": True,
    }
]
