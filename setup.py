import sys
from src import __version__, __author__, __title__
from cx_Freeze import setup, Executable


setup(
    name=__title__,
    version=__version__,
    description="A simple Youtube Music rich presence for Discord",
    author=__author__,
    options={
        "build_exe": {
            "excludes": ["tkinter", "unittest"],
        }
    },
    executables=[
        Executable(
            "main.py",
            copyright="© 2020 - 2023 by " + __author__ + " - All rights reserved",
            icon="assets/icon.ico",
            targetName="Youtube Music Rich Presence.exe",
            shortcutName="Youtube Music RPC",
        )
    ],
)
