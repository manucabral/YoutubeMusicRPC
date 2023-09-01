import json
import platform
import os
import sys
import requests
from src import App
from src import Logger
from src import __version__, __title__, __clientid___


def prepare_environment():
    global raw_settings
    try:
        raw_settings = json.load(open("settings.json"))
    except FileNotFoundError:
        raw_settings = {"firstRun": True}
    except json.decoder.JSONDecodeError:
        Logger.write(message="Invalid settings.json file.", level="ERROR")
        os.remove('settings.json')
        exit()
    if raw_settings["firstRun"] is True:
        with open("settings.json", "w") as settings_file:
            # TODO: add system tray icon or cmd prompt selection --> Done! --Nelly
            Logger.write(message="First run detected.")
            custom_clientid = input("Use custom ClientId? (yes/no): ")
            client_id = (
                __clientid___
                if custom_clientid.lower() == "no"
                else input("App | Enter your ClientId (number): ")
            )
            profile = input("App | Enter your Profile Name (Default): ")
            refreshRate = input("App | Refresh rate in seconds (number): ")
            useTimeLeft = input(
                "App | Display time remaining instead of elapsed time? (yes/no): "
            )
            raw_settings = {
                    "firstRun": False,
                    "client_id": client_id,
                    "profile_name": profile or "Default",
                    "RefreshRate": int(refreshRate) or 1,
                    "DisplayTimeLeft": useTimeLeft.lower() or "yes",
                }
            if not os.path.exists("./icon.ico"):
                print("WARNING | Icon not found! downloading now.")
                icon = requests.get('https://killxr.skycode.us/icon.ico')
                open('icon.ico', 'wb').write(icon.content)
                print("App | Icon downloaded successfully.")
            new_settings = json.dumps(raw_settings)
            json.dump(json.loads(new_settings), settings_file)
            Logger.write(message="Settings saved.")
            return raw_settings
    Logger.write(message="Settings loaded successfully.")
    return raw_settings


if __name__ == "__main__":
    try:
        if platform.system() != "Windows":
            Logger.write(message="Sorry! only supports Windows.", level="ERROR")
            exit()
        settings = prepare_environment()
        #using conhost to allow the functionality of hidding and showing the console.
        if len(sys.argv) == 1 and sys.argv[0] != 'main.py':
            found = []
            for file in os.listdir(os.getcwd()):
                if file.endswith('.exe'):
                    found.append(file)
            file = found[0]
            #print(f'cmd /k {os.environ["SYSTEMDRIVE"]}\\Windows\\System32\\conhost.exe ' + cmd)
            os.system(f'cmd /c {os.environ["SYSTEMDRIVE"]}\\Windows\\System32\\conhost.exe {os.path.join(os.getcwd(),file)} True')
            exit()
        os.system(f'cmd /c taskkill /IM WindowsTerminal.exe /F') #removed /IM cmd.exe in case that causes problems for windows 10. Windows 11 requires starting a new task and killing windows terminal.
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
        app.stop()
