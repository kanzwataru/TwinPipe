import pymel.core as pm

def setup_window():
    win_name = "twinPipeSetupUI"
    if pm.window(win_name, exists=True):
        pm.deleteUI(win_name)

    with pm.window(title="TwinPipe Setup"):
        with pm.verticalLayout():
            pm.button()
            pm.button()
            pm.button()
