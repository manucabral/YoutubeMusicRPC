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
        def remove_preceding_zero(int_as_string: str) -> int:
            if int_as_string.startswith("0") and len(int_as_string) > 1:
                return int(int_as_string[1:])
            return int(int_as_string)

        def filter_time_result_to_seconds(time_result: list[str]) -> int:
            total_seconds: int = 0
            time_length : int = len(time_result)
            if time_length > 3:
                return 0
            includes_hours = time_length == 3 
            if includes_hours:
                for index, time_value in enumerate(time_result):
                    cleaned_time = remove_preceding_zero(time_value)
                    if(index == 0):
                        total_seconds += (cleaned_time * 3600)
                    elif(index == 1):
                        total_seconds += (cleaned_time * 60)
                    elif(index == 2 and includes_hours):
                        total_seconds += cleaned_time
            else:
                for index, time_value in enumerate(time_result):
                    cleaned_time = remove_preceding_zero(time_value)
                    if(index == 0):
                        total_seconds += (cleaned_time * 60)
                    elif(index == 1):
                        total_seconds += cleaned_time
            return total_seconds

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
        retrieval_time = time.time()
        self.playing = self.metadata["playbackState"] == "playing"
        self.pause = self.metadata["playbackState"] == "paused"
        self.ad = self.metadata["advertisement"]
        self.title = filter_metadata(self.metadata["title"])
        self.artist = filter_metadata(self.metadata["artist"])
        self.artwork = self.metadata["artwork"] if self.metadata["artwork"] else "logo"

        times = self.metadata["time"].split(" / ")
        elapsed_seconds = filter_time_result_to_seconds(times[0].split(":"))
        total_seconds = filter_time_result_to_seconds(times[1].split(":"))

        start_time_unix = retrieval_time - elapsed_seconds
        self.start_time = math.trunc(start_time_unix)

        end_time_unix = retrieval_time + total_seconds # Would be end time if just started to play now
        self.projected_end_time = math.trunc(end_time_unix - elapsed_seconds)

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
