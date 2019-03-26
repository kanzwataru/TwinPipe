import maya.cmds as cmds
import pymel.core as pm
import os.path
import subprocess

"""
net use m: /delete
net use m: \\macbook-w7\share\sub qwaszx /user:wataru /persistent:yes
"""

MBOXX_SHARE_PATH = "\\\\macbook-w7\\share\\sub"
MBOXX_MAPPED_LETTER = "m:"
MBOXX_USER = "wataru"
MBOXX_PASS = "qwaszx"

REPO_PATH = os.path.join(MBOXX_MAPPED_LETTER, '__repository__', 'TwinReaperRepo.git')

def bin_dir():
    path = cmds.getModulePath(mn='TwinPipeBootstrap')
    return os.path.normpath(os.path.join(path, 'bin'))

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
    
    path = cmds.fileDialog2(dialogStyle=2, fileMode=3, okCaption='Clone Here')[0]
    if os.listdir(path):
        cmds.warning("Please choose an empty folder to copy into")
        return
    
    subprocess.call("start cmd /k git clone {} {}".format(REPO_PATH, path), shell=True)

def setup_window():
    win_name = "twinPipeSetupUI"
    if pm.window(win_name, exists=True):
        pm.deleteUI(win_name)

    with pm.window(win_name, title="TwinPipe Setup"):
        with pm.verticalLayout():
            pm.button(
                label="Install Git Tools...",
                bgc=(0.5, 0.55, 0.45),
                c=lambda _: git_setup()
            )
            pm.button(
                label="Clone project from mboxx",
                bgc=(0.5, 0.6, 0.65),
                c=lambda _: clone_project()
            )
