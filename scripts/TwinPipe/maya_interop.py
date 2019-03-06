import maya.cmds as cmds


def open_scene(path):
    cmds.NewScene()

    cmds.file(path, open=True)

def reference_scene(path):
    cmds.file(path, reference=True)


def new_scene():
    cmds.file(new=True, force=True)


def import_scene(path):
    raise NotImplementedError


def save_scene(path):
    cmds.file(rename=path)
    cmds.file(save=True)

def get_project():
    return cmds.workspace(q=True, rd=True)

def error_message(msg):
    cmds.warning(msg)

def confirm_ask(title, msg):
    ret = cmds.confirmDialog(
        title=title,
        message=msg,
        button=['Yes','No'],
        defaultButton='Yes',
        cancelButton='No',
        dismissString='No'
    )

    return 'Yes' in ret
