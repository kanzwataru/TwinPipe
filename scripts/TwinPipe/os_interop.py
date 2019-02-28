import os
import os.path
import platform
import subprocess

def show_path(path):
    cmd = {
        'Windows': 'start',
        'Darwin':  'open',
        'Linux':   'xdg-open'
    }[platform.system()]

    if not os.path.isdir(path):
        path = os.path.split(path)[0]

    subprocess.Popen([cmd, os.path.normpath(path)], shell=True)
