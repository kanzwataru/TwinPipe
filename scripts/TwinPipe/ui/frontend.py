from TwinPipe.vendor.Qt import QtCore, QtGui, QtCompat, QtWidgets
from TwinPipe import project
import widgets
reload(project)
reload(widgets)


class TabContents(QtWidgets.QSplitter):
    def __init__(self):
        super(TabContents, self).__init__()

        self.addWidget(widgets.AssetWidget())
        self.addWidget(widgets.EntityWidget())

        self.setOrientation(QtCore.Qt.Vertical)
        self.setChildrenCollapsible(False)


class FrontendWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(FrontendWindow, self).__init__(parent=parent)
        self.resize(800, 600)
        self.setWindowTitle("Twin Reaper Pipeline")

        tabs = QtWidgets.QTabWidget()
        tabs.setStyleSheet("QTabBar::tab { height: 35px; }")

        #tabs.addTab(SceneTab(project.scene_repos), "scenes")
        #tabs.addTab(QtWidgets.QWidget(), "scenes")
        tabs.addTab(TabContents(), project.ASSET_TYPES['scene'])
        for enttype, name in project.ASSET_TYPES.iteritems():
            if enttype == 'scene':
                continue

            tabs.addTab(TabContents(), name)

        #for repo in project.asset_repos:
        #    tabs.addTab(AssetTab(repo), repo.name)

        self.status_bar = QtWidgets.QStatusBar()

        self.setStatusBar(self.status_bar)
        self.setCentralWidget(tabs)
