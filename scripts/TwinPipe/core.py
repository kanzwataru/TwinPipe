from ui import ui_lib, frontend
reload(frontend)

def launch():
	parent = ui_lib.get_maya_window()

	frontend_window = frontend.FrontendWindow(parent)
	ui_lib.show_window('FrontendWindow', frontend_window)
