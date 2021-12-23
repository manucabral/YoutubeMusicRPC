
TITLE = 'YouTube Music RPC'
AUTHOR = 'Manuel Cabral'
VERSION = '0.2'

LINES = 30
COLUMNS = 65

BANNER = (
    """
                     ╦ ╦┌─┐┬ ┬┌┬┐┬ ┬┌┐ ┌─┐
                     ╚╦╝│ ││ │ │ │ │├┴┐├┤ 
                      ╩ └─┘└─┘ ┴ └─┘└─┘└─┘
    """,
    """
                        ╔╦╗┬ ┬┌─┐┬┌─┐      
                        ║║║│ │└─┐││        
                        ╩ ╩└─┘└─┘┴└─┘
    """,
    """
                          ╦═╗╔═╗╔═╗        
                          ╠╦╝╠═╝║          
                          ╩╚═╩  ╚═╝
    """
)

BROWSERS = [
    ('Yandex', 'Yandex Browser', 'browser.exe', 'Chromium', r'\Yandex\YandexBrowser\User Data\Default\History'),
    ('Chrome', 'Google Chrome', 'chrome.exe', 'Chromium', r'\Google\Chrome\User Data\Default\History'),
    ('Edge', 'Microsoft Edge', 'msedge.exe', 'Chromium', r'\Microsoft\Edge\User Data\Default\History'),
]

LANGUAGE = {
    'en': 0,
    'es': 1
}

TOKENS = {
    'Yandex': 'youtube music',
    'Edge': 'youtube\xa0music',
    'Chrome': 'youtube\xa0music'
}
 
MESSAGES = [
    ('Author', 'Autor'),
    ('This version is unstable and not so exact, still development.', 'Esta versión es inestable y no tan exacta, aún en desarrollo.'),
    ('Checking running browsers on your system..', 'Verificando navegadores en ejecución..'),
    ('Browser found:', 'Navegador encontrado:'),
    ('Checking your system language..', 'Verificando el idioma de tu sistema..'),
    ('Language detected:', 'Idioma encontrado:'),
    ('In menu', 'En el menú'),
    ('Pause', 'En pausa'),
    ('Play on Browser', 'Reproducir en tu navegador'),
    ('Download App', 'Descargar aplicación')
]

ERRORS = [
    ('Could not find a running browser', 'No se pudo encontrar un navegador en ejecución'),
    ('Program interrupt by user', 'Programa interrumpido por el usuario'),
    ('Error on generating log file', 'Error al generar el archivo de registro'),
    ('Connection lost, re-connecting in 5 seconds..', 'Conexión perdida, reconectando en 5 segundos..'),
    ('Could not find Discord installed and running on this machine', 'Discord no se encuentra en ejecución o no esta instalado'),
    ('Discord is not running', 'Discord no está en ejecución'),
    ('Could not find your system language', 'No se pudo encontraar el idioma de tu sistema')
]
