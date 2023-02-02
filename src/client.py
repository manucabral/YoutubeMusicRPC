import websocket
import asyncio
import json


class Client:

    __slots__ = ("url", "__ws")
    def __init__(self, url: None):
        self.url = url
        self.__ws = None

    def connect(self):
        self.__ws = websocket.create_connection(self.url, enable_multithread=True)

    def disconnect(self):
        self.__ws.close()

    def call_method(self, method: str, params: dict = {}):
        message = {"id": 1, "method": method, "params": params}
        self.__ws.send(json.dumps(message))
        return self.__ws.recv()
