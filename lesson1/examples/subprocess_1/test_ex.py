"""Получение кода завершения подпроцесса"""

import platform
from subprocess import Popen

PROGRAM = 'notepad.exe' if platform.system().lower() == 'windows' else 'libreoffice'
PROCESS = Popen(PROGRAM)
