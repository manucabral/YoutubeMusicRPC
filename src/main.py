from colorama import Fore as color, init as colorama_init
from subprocess import check_output as co, PIPE
from os import system
from sys import exit
from time import sleep, time
from datetime import datetime
from pypresence import Presence, exceptions as rpcexceptions
from browser import Browser
from constants import *
from exceptions import *

class YoutubeMusicRPC:
  running = False

  def __init__(self, client_id: str, lang: str):
    self.__client_id = client_id
    self.lang = LANGUAGE[lang]
    self.start_time = self.prev_music = self.browser = None
  
  def _write_log(self, msg: str) -> None:
    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    try:
      with open('log.txt', 'a', encoding='utf-8') as file:
        fullmsg = f'[{time}] {msg}\n'
        file.write(fullmsg)
      file.close()
    except Exception:
      self._message(ERRORS[2][self.lang], type='error')

  def _message(self, msg: str, type: str = 'info', log: bool = False) -> None:
    keys = {
      'info': (color.LIGHTCYAN_EX, '>'),
      'success': (color.GREEN, '✓'),
      'error': (color.RED, 'X')
    }
    data = keys[type]
    print(f'{color.WHITE}[{data[0]}{data[1]}{color.WHITE}] {msg}{color.RESET}')
    if log:
      self._write_log(msg)
    
  def _get_browsers(self) -> []:
    browsers = []
    for browser in BROWSERS:
      query = f'WMIC PROCESS WHERE "name=\'{browser[2]}\'" GET ExecutablePath'
      result = co(query, universal_newlines=True, stderr=PIPE)
      browsers.append(browser) if browser[0].lower() in result.lower() else None
    return browsers

  def _set_title(self) -> None:
    system('title ' + TITLE)
    system(f'mode con:cols={COLUMNS} lines={LINES}')

  def _check_browsers(self) -> None:
    self._message(MESSAGES[2][self.lang], type='info')
    browsers = self._get_browsers()
    if not browsers:
      raise BrowserNotFound()
    if len(browsers) == 1:
      browser = browsers[0]
      self.browser = Browser(name=browser[0], fullname=browser[1], process=browser[2], base=browser[3], path=browser[4])
      self._message(f'{MESSAGES[3][self.lang]} {self.browser.fullname} ({self.browser.process})', type='success')
  
  def _check_system_lang(self) -> None:
    self._message(MESSAGES[4][self.lang], type='info')
    lang = co('powershell get-uiculture', universal_newlines=True, stderr=PIPE).split('\n')[3][17:].split('           ')
    self.system_lang = (lang[0], lang[1][1:])
    if not lang[0]:
      raise SystemLanguageNotFound()
    self._message(f'{MESSAGES[5][self.lang]} {self.system_lang[1]}', type='success')
  
  def _initialize(self) -> None:
    colorama_init()
    system('cls')
    self._set_title()

  def _display_logo(self):
    print(color.RED, BANNER[0], color.WHITE, BANNER[1], color.LIGHTCYAN_EX, BANNER[2], color.RESET)
    print('Version:', VERSION)
    print(f'{MESSAGES[0][self.lang]}:', AUTHOR)
    print(f'{MESSAGES[1][self.lang]}')
    print()
  
  def _get_author(self, title: str) -> str:
    tokens = title.split('-')
    if len(tokens) == 1:
      return None
    return tokens[0] 

  def _get_detail(self, title: str, url: str) -> str:
    tokens = title.split('-')
    if len(tokens) == 1:
      return MESSAGES[7][self.lang]
    if url == 'https://music.youtube.com/':
      return MESSAGES[6][self.lang] 
    if TOKENS[self.browser.name] in tokens[1].lower():
      return 'Artist'
    return tokens[1]
  
  def _get_buttons(self, details: str, url: str) -> []:
    buttons = []
    if details != MESSAGES[6][self.lang]:
      buttons.append({"label": MESSAGES[8][self.lang], "url": url})
    buttons.append({"label": MESSAGES[9][self.lang], "url": "https://github.com/manucabral/YoutubeMusicRPC"})
    return buttons
  
  def _handler(self, data) -> None:
    title, url = data[0], data[1]
    state = start_time = None
    details = self._get_detail(title, url)
    state = self._get_author(title)
    buttons = self._get_buttons(details, url)
    if title != self.prev_music:
      self.start_time = None if title.lower() == 'youtube music'.lower() else time()
      self.prev_music = title
    return {
      'state': state,
      'details': details,
      'start': self.start_time,
      'large_image': 'logo',
      'large_text': 'YouTube Music',
      'buttons': buttons
    }
  
  def _update_presence(self) -> None:
    data = self.browser.current_website()
    if not data:
      data = {
        'details': 'Offline',
        'large_image': 'logo'
      }
    else:
      data = self._handler(data)
    self.__presence.update(**data)

  def _main_event(self) -> None:
    while self.running:
      if not self.browser.running():
        raise BrowserNotFound()
      self._update_presence()
      sleep(15)

  def stop(self) -> None:
    self.running = False
    exit()

  def _rpc_connect(self) -> None:
    try:
      self.__presence = Presence(self.__client_id)
      self.__presence.connect()
    except rpcexceptions.DiscordNotFound:
      self._message(ERRORS[4][self.lang], type='error', log=True)
    except rpcexceptions.InvalidPipe:
      self._message(ERRORS[5][self.lang], type='error', log=True)
    
  def run(self) -> None:
    try:
      self._initialize()
      self._display_logo()
      self._check_system_lang()
      self._check_browsers()
    except BrowserNotFound:
      self._message(ERRORS[0][self.lang], type='error', log=True)
      self.stop()
    except SystemLanguageNotFound:
      self._message(ERRORS[6][self.lang], type='error', log=True)
      self.stop()
    self.running = True
    try:
      self._rpc_connect()
      self._main_event()
    except rpcexceptions.InvalidID:
      self._message(ERRORS[5][self.lang], type='error', log=True)
      self.stop()
    except BrokenPipeError:
      self._message(ERRORS[5][self.lang], type='error', log=True)
      self.stop()
    except KeyboardInterrupt:
      self._message(ERRORS[1][self.lang], type='error')
      self.__presence.close()
      self.stop()
    except BrowserNotFound:
      self._message(ERRORS[0][self.lang], type='error', log=True)
      self.__presence.close()
      self.run()
