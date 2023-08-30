import platform
from src import App
from src import Logger
from src import __version__, __title__
import json

if __name__ == "__main__":
    try:
        if platform.system() != "Windows":
            Logger.write(message="Sorry! only supports Windows.", level="ERROR")
            exit()
        with open('settings.json') as json_file:
            raw_settings = json.load(json_file)
            if raw_settings["firstRun"] == True:
                clientId = input(" App | Enter your ClientId (number): ")
                profile = input(" App | Enter your Profile Name (Default): ")
                refreshRate = input(" App | Refresh rate in seconds (number): ")
                useTimeLeft = input(" App | Display time remaining instead of elapsed time? (yes/no): ")
                newSettings =  json.dumps({
                    "firstRun": False,
                    "client_id": clientId or raw_settings["client_id"],
                    "profile_name": profile or "Default",
                    "RefreshRate": int(refreshRate) or 1,
                    "DisplayTimeLeft": useTimeLeft.lower() or "yes"
                 })
                with open('settings.json', 'w') as outfile:
                    outfile.write(newSettings)
 
        settings = json.load(open('settings.json'))
        app = App(
            client_id= settings["client_id"],
            version=__version__,
            title=__title__,
            profileName= settings["profile_name"],
            refreshRate= settings["RefreshRate"],
            useTimeLeft= settings["DisplayTimeLeft"]
        )
        app.sync()
        app.run()
    except KeyboardInterrupt:
        Logger.write(message="User interrupted.")
    input("Press any key to continue...")
