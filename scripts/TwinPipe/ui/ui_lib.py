import os
import types
from TwinPipe.vendor.Qt import QtCore, QtGui, QtCompat, QtWidgets
from maya import OpenMayaUI

glb_open_windows = {}

def get_maya_window():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    widget = QtCompat.wrapInstance(long(ptr), QtWidgets.QWidget)

    return widget

def get_path(*args):
    base = os.path.split(__file__)[0]
    return os.path.join(base, *args)

def create_ui(classtype, *args, **kwargs):
    assert(hasattr(classtype, 'setup'))

    uifile = classtype.uifile
    ui = QtCompat.loadUi(get_path(*uifile))

    for member in dir(classtype):
        if hasattr(getattr(classtype, member), '__func__'):
            func = getattr(classtype, member).__func__
            setattr(ui, member, types.MethodType(func, ui))

    ui.setup(*args, **kwargs)
    return ui

def show_window(name, window):
    if name in glb_open_windows:
        glb_open_windows[name].destroy()

    glb_open_windows[name] = window
    glb_open_windows[name].show()
