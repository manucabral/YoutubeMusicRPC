import json
import datetime
from .client import Client


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
        if data["value"] is None:
            return None
        return json.loads(response)["result"]["result"]["value"].split("#")

    def connect(self):
        if not self.connected:
            self.__connection.connect()
            self.connected = True

    def sync(self):
        if not self.connected:
            raise Exception("Tab is not connected")
        self.metadata = self.__parse_response(
            self.__execute(
                "Runtime.evaluate",
                {
                    "expression": "navigator.mediaSession.metadata && [\
                        navigator.mediaSession.playbackState, \
                        navigator.mediaSession.metadata.title, \
                        navigator.mediaSession.metadata.artist, \
                        navigator.mediaSession.metadata.album, \
                        navigator.mediaSession.metadata.artwork[0].src, \
                        document.querySelector('#left-controls > span').textContent.trim(),\
                        document.querySelector('.badge-style-type-ad-stark').hidden,\
                    ].join([separator = '#'])"
                },
            )
        )
        if not self.metadata:
            self.pause = False
            return
        self.ad = self.metadata[6] == "false"
        self.playing = self.metadata[0] == "playing"
        self.pause = self.metadata[0] == "paused"
        self.title = self.metadata[1] if self.metadata[1] else "Unknown"
        self.artist = self.metadata[2] if self.metadata[2] else "Unknown"
        self.album = self.metadata[3] if self.metadata[3] else "Unknown"
        self.artwork = self.metadata[4] if self.metadata[4] else "logo"
        if "http" in self.metadata[5]:
            self.start = self.end = 1
            self.artist = "Advertisement"
            return
        # TODO: parse times to unix epoch
        times = self.metadata[5].split(" / ")

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
