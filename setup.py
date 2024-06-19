import sys
from src import __version__, __author__, __title__
from cx_Freeze import setup, Executable


setup(
    name=__title__,
    version=__version__,
    # description displays in the notification for some reason
    description="YT Music RPC",
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
            icon="assets/new_logo.ico",
            target_name="Youtube Music Rich Presence",
            shortcut_name="Youtube Music RPC",
        )
    ],
)
