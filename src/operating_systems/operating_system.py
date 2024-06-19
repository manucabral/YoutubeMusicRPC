from abc import ABC, abstractmethod

class OperatingSystem(ABC):
    """
    Abstract class for functionality 
    that differs between operating systems
    """

    @abstractmethod
    def get_default_browser(self) -> dict:
        """
        Returns the user' default browser metadata in a dictionary
        """
        pass

    @abstractmethod
    def is_browser_running(self) -> bool:
        pass

    @abstractmethod
    def run_browser_with_debugging_server(self, profile_name: str) -> None:
        """
        Starts a browser with debugging enabled.
        profile_name should correspond with the user profile 
        """
        pass

    @abstractmethod
    def get_browser_process_name(self) -> str:
        pass

    @abstractmethod
    def hide_console_process(self) -> str:
        pass