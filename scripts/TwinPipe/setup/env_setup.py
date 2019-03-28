import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import os.path
import subprocess

"""
net use m: /delete
net use m: \\macbook-w7\share\sub qwaszx /user:wataru /persistent:yes
"""

MBOXX_SHARE_PATH = "\\\\mboxx\\3rd_year_films\\TwinReaper"
MBOXX_MAPPED_LETTER = "m:"
MBOXX_USER = "3duser"
MBOXX_PASS = "d4ws0n"

REPO_PATH = os.path.join(MBOXX_MAPPED_LETTER, '__repository__', 'TwinReaperRepo.git')
PROJECT_NAME = 'TwinReaper'

def bin_dir():
    path = cmds.getModulePath(mn='TwinPipeBootstrap')
    return os.path.normpath(os.path.join(path, 'bin'))

def git():
    path = bin_dir()
    git_path = os.path.normpath(os.path.join(path, 'git','bin','git.exe'))
    return git_path

def mboxx_setup():
    try:
        subprocess.call("net use {} /delete".format(MBOXX_MAPPED_LETTER))
    except OSError:
        pass
    
    subprocess.call("net use {} {} {} /user:{} /persistent:yes".format(
        MBOXX_MAPPED_LETTER,
        MBOXX_SHARE_PATH,
        MBOXX_PASS,
        MBOXX_USER))

def git_setup():
    bat = os.path.join(bin_dir(), 'windows_tools', 'install.bat')
    subprocess.call("start {}".format(bat), shell=True)

def clone_project():
    mboxx_setup()
    
    path = cmds.fileDialog2(dialogStyle=2, fileMode=3, okCaption='Clone Here')
    if not path:
        return

    path = path[0]
    clone_path = os.path.normpath(os.path.join(path, PROJECT_NAME))
    
    subprocess.call("start cmd /k {} clone {} {}".format(git(), REPO_PATH, clone_path), shell=True)

def set_project():
    mel.eval('SetProject')

def setup_window():
    win_name = "twinPipeSetupUI"
    if pm.window(win_name, exists=True):
        pm.deleteUI(win_name)

    with pm.window(win_name, title="TwinPipe Setup", height=400):
        with pm.verticalLayout():
            pm.button(
                label="Install Git Tools...",
                bgc=(0.5, 0.6, 0.4),
                c=lambda _: git_setup()
            )
            pm.button(
                label="Clone Project from MBOXX",
                bgc=(0.5, 0.6, 0.65),
                c=lambda _: clone_project()
            )
            pm.button(
                label="Set Project",
                bgc=(0.4, 0.55, 0.45),
                c=lambda _: set_project()
            )
            pm.separator()
            pm.button(
                label="Map MBOXX to M:\\ drive",
                c=lambda _: mboxx_setup()
            )
