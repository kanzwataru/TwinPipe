import maya.cmds as cmds


def open_scene(path):
    raise NotImplementedError


def reference_scene(path):
    raise NotImplementedError


def import_scene(path):
    raise NotImplementedError


def save_scene(path):
    raise NotImplementedError


def get_project():
    return cmds.workspace(q=True, rd=True)

def error_message(msg):
    cmds.warning(msg)
