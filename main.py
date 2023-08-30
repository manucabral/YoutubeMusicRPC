import json
import platform
from src import App
from src import Logger
from src import __version__, __title__, __clientid___


def prepare_environment():
    try:
        raw_settings = json.load(open("settings.json"))
    except FileNotFoundError:
        raw_settings = {"firstRun": True}
    except json.decoder.JSONDecodeError:
        Logger.write(message="Invalid settings.json file.", level="ERROR")
        exit()
    with open("settings.json", "w") as settings_file:
        if raw_settings["firstRun"] is True:
            # TODO: add system tray icon or cmd prompt selection
            Logger.write(message="First run detected.", origin=__name__)
            custom_clientid = input("Use custom ClientId? (yes/no): ")
            client_id = (
                __clientid___
                if custom_clientid.lower() == "no"
                else int(input("App | Enter your ClientId (number): "))
            )
            profile = input("App | Enter your Profile Name (Default): ")
            refreshRate = input("App | Refresh rate in seconds (number): ")
            useTimeLeft = input(
                "App | Display time remaining instead of elapsed time? (yes/no): "
            )
            new_settings = json.dumps(
                {
                    "firstRun": False,
                    "client_id": client_id,
                    "profile_name": profile or "Default",
                    "RefreshRate": int(refreshRate) or 1,
                    "DisplayTimeLeft": useTimeLeft.lower() or "yes",
                }
            )
            settings_file.write(new_settings)
    return json.load(open("settings.json"))


if __name__ == "__main__":
    try:
        if platform.system() != "Windows":
            Logger.write(message="Sorry! only supports Windows.", level="ERROR")
            exit()
        settings = prepare_environment()
        app = App(
            client_id=settings["client_id"],
            version=__version__,
            title=__title__,
            profileName=settings["profile_name"],
            refreshRate=settings["RefreshRate"],
            useTimeLeft=settings["DisplayTimeLeft"],
        )
        app.sync()
        app.run()
    except KeyboardInterrupt:
        Logger.write(message="User interrupted.")
    input("Press any key to continue...")
