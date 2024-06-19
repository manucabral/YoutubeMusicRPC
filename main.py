import json
import platform
import os
import httpx
from src import App
from src.operating_systems.operating_system import OperatingSystem
from src.operating_systems.windows_operating_system import WindowsOperatingSystem
from src.operating_systems.linux_operating_system import LinuxOperatingSystem
from src.notifiers.notifier import Notifier
from src.notifiers.windows_notifier import WindowsNotifier
from src import Logger
from src import __version__, __title__, __clientid___

def prepare_environment():
    try:
        raw_settings = json.load(open("settings.json"))
    except FileNotFoundError:
        raw_settings = {"first_run": True}
    except json.decoder.JSONDecodeError:
        Logger.write(message="Invalid settings.json file.", level="ERROR")
        os.remove("settings.json")
        exit()
    if raw_settings["first_run"] is True:
        with open("settings.json", "w") as settings_file:
            Logger.write(message="First run detected.")
            custom_clientid = input("Use custom ClientId? (yes/no): ")
            client_id = (
                __clientid___
                if custom_clientid.lower() == "no"
                else input("App | Enter your ClientId (number): ")
            )
            profile = input("App | Enter your Profile Name (Default): ")
            #TODO: Sanitize refresh rate input, will crash if NaN
            refresh_rate = input("App | Refresh rate in seconds (number): ")
            use_time_left_choice = input(
                "App | Display time remaining instead of elapsed time? (yes/no): "
            )
            raw_settings = {
                "first_run": False,
                "client_id": client_id,
                "profile_name": profile or "Default",
                "refresh_rate": int(refresh_rate) or 1,
                "display_time_left": True if use_time_left_choice.lower() == "yes" else False,
            }
            if not os.path.exists("./icon.ico"):
                print("WARNING | Icon not found! downloading now.")
                icon = httpx.get("https://killxr.skycode.us/icon.ico")
                open("icon.ico", "wb").write(icon.content)
                print("App | Icon downloaded successfully.")
            new_settings = json.dumps(raw_settings)
            json.dump(json.loads(new_settings), settings_file)
            Logger.write(message="Settings saved.")
            return raw_settings
    Logger.write(message="Settings loaded successfully.")
    return raw_settings


if __name__ == "__main__":
    try:
        operating_system: str = platform.system()
        system: OperatingSystem = None
        notifier: Notifier = None
        match operating_system:
            case "Windows":
                system = WindowsOperatingSystem()
                notifier = WindowsNotifier()
            case "Linux":
                system = LinuxOperatingSystem()
            case _:
                Logger.write(message="Sorry! only supports Windows and Linux.", level="ERROR")
                exit()
        settings = prepare_environment()
        system.hide_console_process()
        app = App(
            operating_system=system,
            notifier=notifier,
            client_id=settings["client_id"],
            version=__version__,
            title=__title__,
            profileName=settings["profile_name"],
            refreshRate=settings["refresh_rate"],
            useTimeLeft=settings["display_time_left"],
        )
        app.sync()
        app.run()
    except KeyboardInterrupt:
        Logger.write(message="User interrupted.")
        app.stop()