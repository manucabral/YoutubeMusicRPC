class YoutubeRPCException(Exception):
    def __init__(self, message: str = None):
        if message is None:
            message = 'An error has occurred within Youtube RPC'
        super().__init__(message)

class BrowserNotFound(YoutubeRPCException):
    def __init__(self):
        super().__init__('Could not find a running browser')

class SystemLanguageNotFound(YoutubeRPCException):
    def __init__(self):
        super().__init__('Could not find your system language')