import json
import time
from .client import Client
import math


class Tab:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.connected = False
        self.playing = False
        self.__connection = Client(self.webSocketDebuggerUrl)

    def __repr__(self) -> str:
        return f"<Tab {self.id}>"

    def __parse_response(self, response: str) -> dict:
        data = json.loads(response)["result"]["result"]
        return data["value"]

    def connect(self):
        if not self.connected:
            self.__connection.connect()
            self.connected = True

    def sync(self):
        global LastTime
        LastTime = 4

        def filterZeros(string: str):
            if string.startswith("0") and len(string) > 1:
                return int(string[1:])
            return int(string)

        def checkForUpdate(eclapsedTime):
            if returnTimeInUnix(eclapsedTime) == LastTime:
                startUnixTime = time.time()
                return startUnixTime
            return

        def returnTimeInUnix(dict: dict):
            global TimeInUnix
            global timeType
            timeType = "Minutes"
            TimeInUnix = 0
            if len(dict) == 3:
                timeType = "Hours"
            elif len(dict) == 2:
                timeType = "Minutes"

            if timeType == "Hours":
                for x in range(0, len(dict), 1):
                    filteredNumber = filterZeros(dict[x])
                    if x == 0:
                        TimeInUnix = TimeInUnix + (filteredNumber * 3600)
                    elif x == 1:
                        TimeInUnix = TimeInUnix + (filteredNumber * 60)
                    elif x == 2:
                        TimeInUnix = TimeInUnix + filteredNumber
                return TimeInUnix
            if timeType == "Minutes":
                for x in range(0, len(dict), 1):
                    filteredNumber = filterZeros(dict[x])
                    if x == 0:
                        TimeInUnix = TimeInUnix + (filteredNumber * 60)
                    elif x == 1:
                        TimeInUnix = TimeInUnix + filteredNumber
                return TimeInUnix

        def filter_metadata(metadata: str):
            """Adds empty char to 1 len metadata as PyPresence does not allow 1 len"""
            if not metadata or metadata == "": return "Unknown" 
            if len(metadata) == 1:
                return metadata + chr(0)
            return metadata
        if not self.connected:
            raise Exception("Tab is not connected")
        self.metadata = self.__parse_response(
            self.__execute(
                "Runtime.evaluate",
                {
                    "expression": """
                        navigator.mediaSession.metadata && {
                            "playbackState"   : navigator.mediaSession.playbackState, 
                            "title"     : navigator.mediaSession.metadata.title, 
                            "artist"    : navigator.mediaSession.metadata.artist, 
                            "album"     : navigator.mediaSession.metadata.album, 
                            "artwork"   : navigator.mediaSession.metadata.artwork[0].src, 
                            "time"      : document.querySelector('#left-controls > span').textContent.trim(),
                            "advertisement"        : !document.querySelector('.badge-style-type-ad-stark').hidden,
                        }
                    """,
                    "returnByValue": True
                },
            )
        )
        if not self.metadata:
            self.pause = False
            return
        self.playing = self.metadata["playbackState"] == "playing"
        self.pause = self.metadata["playbackState"] == "paused"
        self.ad = self.metadata["advertisement"]
        self.title = filter_metadata(self.metadata["title"])
        self.artist = filter_metadata(self.metadata["artist"])
        self.artwork = self.metadata["artwork"] if self.metadata["artwork"] else "logo"

        times = self.metadata["time"].split(" / ")
        eclapsedTime = times[0].split(":")
        timeLeft = times[1].split(":")
        startUnixTime = time.time() - returnTimeInUnix(eclapsedTime)
        EndUnixTime = time.time() + returnTimeInUnix(timeLeft)
        LastTime = math.trunc(returnTimeInUnix(eclapsedTime))
        self.start = math.trunc(startUnixTime)
        self.end = math.trunc(EndUnixTime - returnTimeInUnix(eclapsedTime))

    def close(self):
        if self.connected:
            self.__connection.disconnect()
            self.connected = False

    def __execute(self, method: str, params: dict = {}):
        return self.__connection.call_method(method, params)

    def __eq__(self, other):
        if other is None:
            return False
        return (
            self.url == other.url
            and self.playing == other.playing
            and self.pause == other.pause
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def update(self):
        self.connect()
        self.sync()
        self.close()
