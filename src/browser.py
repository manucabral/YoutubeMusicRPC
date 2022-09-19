from os import getenv, path, system
from subprocess import check_output as co, PIPE
from shutil import copy2
import sqlite3


class Browser:
    def __init__(self, **args):
        self.name = args.get('name', None)
        self.fullname = args.get('fullname', None)
        self.process = args.get('process', None)
        self.base = args.get('base', None)
        self.last_website = self.time = None
        self.path = getenv('LOCALAPPDATA') + args.get('path', '')
        self.temp_path = getenv('TEMP') + '\\' + args['path'].split('\\')[5]

    def _update_history(self) -> None:
        if path.isfile(self.temp_path):
            system(f'del {self.temp_path}')
        copy2(self.path, self.temp_path)

    def _execute_query(self, path: str, query: str) -> tuple:
        try:
            cursor = sqlite3.connect(path).cursor()
            result = [r for r in cursor.execute(query)]
            cursor.close()
            return result[0]
        except Exception as e:
            print('An error ocurred', e)

    def running(self) -> bool:
        return True if self.name.lower() in co(f'wmic process where "name=\'{self.process}\'" get ExecutablePath', universal_newlines=True, stderr=PIPE).lower() else False

    def current_website(self) -> tuple:
        token = 'music.youtube.com'
        self._update_history()
        result = self._execute_query(
            self.temp_path, 'SELECT title, url, datetime(last_visit_time / 1000000 + (strftime("%s", "1601-01-01")), "unixepoch", "localtime") from urls ORDER BY last_visit_time DESC limit 1')
        if token in result[1]:
            self.last_website = result
            return result
        if self.last_website:
            return self.last_website
        return None
