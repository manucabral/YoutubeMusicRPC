import platform
from src import App
from src import Logger


if __name__ == "__main__":
    try:
        if platform.system() != "Windows":
            Logger.write(message="Sorry! only supports Windows.", level="ERROR")
            exit()
        app = App(client_id="superclient")
        app.sync()
        app.run()
    except KeyboardInterrupt:
        Logger.write(message="User interrupted.")
    input("Press any key to continue...")