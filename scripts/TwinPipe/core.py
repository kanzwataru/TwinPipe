import project
import maya_interop as dcc
from ui import ui_lib, frontend
reload(frontend)
reload(dcc)

def launch():
    path = dcc.get_project()
    try:
        proj = project.Project.load(path)
    except ValueError:
        dcc.error_message("Current project is not TwinPipe compatible")
        return

    parent = ui_lib.get_maya_window()

    frontend_window = frontend.FrontendWindow(proj, parent)
    ui_lib.show_window('FrontendWindow', frontend_window)
