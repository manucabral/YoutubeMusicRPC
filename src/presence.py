import pypresence as pp
from .logger import Logger


class Presence:
    __slots__ = ("__client_id", "__rpc")

    def __init__(self, client_id: str = None):
        self.__rpc = None
        self.__client_id = client_id
        Logger.write(message="initialized.", origin=self)

    def __handle_exception(self, exc: Exception):
        Logger.write(message=exc, level="ERROR", origin=self)

    def connect(self) -> None:
        try:
            self.__rpc = pp.Presence(self.__client_id)
            self.__rpc.connect()
            Logger.write(message="connected.", origin=self)
            return True
        except Exception as exc:
            self.__handle_exception(exc)
            return False

    def connected(self) -> bool:
        return self.__rpc.connected

    def close(self) -> None:
        try:
            self.__rpc.close()
            Logger.write(message="closed.", origin=self)
        except Exception as exc:
            self.__handle_exception(exc)

    def update(self, **kwargs) -> None:
        try:
            self.__rpc.update(**kwargs)
            Logger.write(message="updated.", origin=self)
        except Exception as exc:
            self.__handle_exception(exc)
