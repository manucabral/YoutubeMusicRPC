import datetime


class Logger:
    @staticmethod
    def write(**kwargs):
        message = kwargs.get("message", "No message provided.")
        level = kwargs.get("level", "INFO")
        origin = kwargs.get("origin", "Unknown").__class__.__name__
        output = f"{level.upper()} | {origin}: {message}"
        print(output)
        with open("client.log", "a", encoding="utf-8") as file:
            now = datetime.datetime.now()
            formated = now.strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{formated}] {output} \r")
