import os
import subprocess as sp
from src.operating_systems.operating_system import OperatingSystem
from ..utils import find_browser_by_process, run_browser

class LinuxOperatingSystem(OperatingSystem):

    __slots__ = (
        "browser_process_name",
        "browser_executable_path",
    )

    def get_default_browser(self) -> dict:
        default_browser_capture = sp.run(
            ["xdg-settings", "get", "default-web-browser"],
            capture_output=True,
            text=True
        )
        if default_browser_capture.stderr != "":
            raise Exception("Can't find default browser")
        default_browser = default_browser_capture.stdout.split(".")[0]
        found_browser = find_browser_by_process("linux", default_browser)
        self.browser_process_name = found_browser["process"]['linux']
        if not found_browser:
            raise Exception("Unsupported browser, sorry")

        browser_path_capture = sp.run(
            ["which", default_browser],
            capture_output=True,
            text=True
        )
        if browser_path_capture.stderr != "":
            raise Exception("Cannot find browser executable location")

        found_browser["path"] = browser_path_capture.stdout.split("\n")[0]
        self.browser_executable_path = browser_path_capture.stdout.split("\n")[0]
        return found_browser

    def is_browser_running(self) -> bool:
        # FIXME: When installing chrome through .deb its process name will be "chrome" and not "google-chrome"
        # Perhaps change ["process"][key] to list in BROWSER array
        process_name = self.browser_process_name
        if process_name == "google-chrome":
            process_name = "chrome"
        all_processes = sp.run(['ps', '-e'], capture_output=True)
        chrome_processes = sp.run(['grep', process_name], input=all_processes.stdout, capture_output=True)
        # FIXME: only tested on chrome, 'chrome_crashpad' will linger after the browser closed
        filtered_chrome_processes = sp.run(['grep', '-v', 'chrome_crashpad'], 
                                        input=chrome_processes.stdout, 
                                        capture_output=True).stdout.decode()
        if filtered_chrome_processes is not None and filtered_chrome_processes != "":
            return True
        return False

    def run_browser_with_debugging_server(self, profile_name: str) -> None:
        user_home = os.path.expanduser('~')
        profile_path = os.path.join(user_home, '.config', 'google-chrome', 'Default')
        run_browser(
            self.browser_executable_path,
            profile_name,
            profile_path
            )

    def get_browser_process_name(self) -> bool:
        return self.browser_process_name

    def hide_console_process(self) -> str:
        # TODO: Implement
        pass