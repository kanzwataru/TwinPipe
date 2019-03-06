from TwinPipe.vendor.Qt import QtCore, QtGui, QtCompat, QtWidgets
from TwinPipe import project
import widgets
reload(project)
reload(widgets)


class TabContents(QtWidgets.QSplitter):
    def __init__(self, proj, atype):
        super(TabContents, self).__init__()

        entity_widget = widgets.EntityWidget()
        asset_widget = widgets.AssetWidget(proj, atype, entity_widget)

        self.addWidget(asset_widget)
        self.addWidget(entity_widget)

        self.setOrientation(QtCore.Qt.Vertical)
        self.setChildrenCollapsible(False)


class FrontendWindow(QtWidgets.QMainWindow):
    def __init__(self, proj, parent=None):
        super(FrontendWindow, self).__init__(parent=parent)
        self.proj = proj

        self.resize(800, 600)
        self.setWindowTitle("Twin Reaper Pipeline")

        tabs = QtWidgets.QTabWidget()
        tabs.setStyleSheet("QTabBar::tab { height: 35px; }")

        #tabs.addTab(SceneTab(project.scene_repos), "scenes")
        #tabs.addTab(QtWidgets.QWidget(), "scenes")

        tabs.addTab(TabContents(proj, 'scene'), project.ASSET_TYPES['scene'])

        for atype, name in project.ASSET_TYPES.iteritems():
            if atype == 'scene':
                continue

            tabs.addTab(TabContents(proj, atype), name)

        #for repo in project.asset_repos:
        #    tabs.addTab(AssetTab(repo), repo.name)

        self.status_bar = QtWidgets.QStatusBar()

        self.setStatusBar(self.status_bar)
        self.setCentralWidget(tabs)
