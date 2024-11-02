from abc import ABC, abstractmethod
class SystemTray(ABC):
    @abstractmethod
    def start() -> None:
        pass

    def stop() -> None:
        pass