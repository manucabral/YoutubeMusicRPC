class Logger:
    
    @staticmethod
    def write(**kwargs):
        message = kwargs.get("message", "No message provided.")
        level = kwargs.get("level", "INFO")
        origin = kwargs.get("origin", "Unknown").__class__.__name__
        print(f"{level.upper()} | {origin}: {message}")
