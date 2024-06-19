import sys
import os
try:
    import winreg as wr
except ImportError:
    pass
from src.operating_systems.operating_system import OperatingSystem
from ..utils import find_browser, run_browser 

class WindowsOperatingSystem(OperatingSystem):

    __slots__ = (
        "browser_process_name",
        "browser_executable_path",
        "browser_profile_path",
    )

    def get_default_browser(self) -> bool:
        progid = wr.QueryValueEx(
            wr.OpenKey(
                wr.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice",
            ),
            "ProgId",
        )[0]
        if not progid:
            raise Exception("Can't find default browser")
        browser = find_browser("name", progid.split(".")[0])
        if not browser:
            raise Exception("Unsupported browser, sorry")
        browser["path"] = wr.QueryValueEx(
            wr.OpenKey(wr.HKEY_CLASSES_ROOT, progid + "\shell\open\command"), ""
        )[0].split('"')[1]
        self.browser_executable_path = browser["path"]
        self.browser_process_name = browser["process"]["win32"]
        self.browser_profile_path = browser["profilePath"]
        return browser

    def is_browser_running(self) -> bool:
        #FIXME: This implementation is broken (see issue #41)
        return False
        """
        res = sp.check_output(
            "WMIC PROCESS WHERE \"name='{process_name}'\" GET Execu wtablePath",
            stderr=sp.PIPE,
        ).decode()
        return bool(re.search(ref, res))
        """

    def run_browser_with_debugging_server(self, profile_name:str) -> None:
        full_profile_path = f'{os.environ["systemdrive"]}\\users\\{os.getenv("username") + self.browser_profile_path + profile_name}'
        run_browser(
            self.browser_executable_path,
            profile_name,
            full_profile_path
            )

    def get_browser_process_name(self) -> str:
        return self.browser_process_name
    
    def hide_console_process(self) -> str:
        # FIXME: Ugly implementation, there are alternatives for this
        # using conhost to allow the functionality of hidding and showing the console.
        if len(sys.argv) == 1 and not sys.argv[0].endswith("main.py"):
            found = []
            for file in os.listdir(os.getcwd()):
                if file.endswith(".exe"):
                    found.append(file)
            file = found[0]
            # print(f'cmd /k {os.environ["SYSTEMDRIVE"]}\\Windows\\System32\\conhost.exe ' + cmd)
            os.system(
                f'cmd /c {os.environ["SYSTEMDRIVE"]}\\Windows\\System32\\conhost.exe {os.path.join(os.getcwd(),file)} True'
            )
            exit()
        os.system(
            f"cmd /c taskkill /IM WindowsTerminal.exe /IM cmd.exe /F"
        )  # removed /IM cmd.exe in case that causes problems for windows 10. Windows 11 requires starting a new task and killing windows terminal.
