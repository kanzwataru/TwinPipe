from TwinPipe import project
from TwinPipe.vendor.Qt import QtCore, QtGui, QtCompat, QtWidgets
import TwinPipe.maya_interop as dcc
import dialogs
reload(dialogs)

def button(label):
    btn = QtWidgets.QPushButton(label)
    btn.setMinimumSize(38, 38)

    return btn


class TableWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout()
        self.button_bar_layout = QtWidgets.QVBoxLayout()
        self.button_bar_widget = QtWidgets.QWidget()
        self.button_bar_widget.setLayout(self.button_bar_layout)

        self.vertical_layout = QtWidgets.QVBoxLayout()
        vertical_widget = QtWidgets.QWidget()
        vertical_widget.setLayout(self.vertical_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.vertical_layout.addWidget(self.table)

        self.add_button = button('+')
        self.remove_button = button('-')
        self.button_bar_layout.addWidget(self.add_button)
        self.button_bar_layout.addWidget(self.remove_button)
        self.button_bar_layout.addStretch()

        layout.addWidget(vertical_widget)
        layout.addWidget(self.button_bar_widget)
        self.setLayout(layout)


class AssetWidget(TableWidget):
    def __init__(self, proj, atype, entity_widget, parent=None):
        super(AssetWidget, self).__init__(parent)
        self.entity_widget = entity_widget
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Name', 'Status', 'Latest Log'])
        self.table.itemSelectionChanged.connect(self.selection_changed)

        self.proj = proj
        self.atype = atype

        self.add_button.clicked.connect(self.new_asset)
        self.remove_button.clicked.connect(self.delete_asset)

        self.reload()

    def reload(self):
        self.current_asset = None
        self.assets = self.proj.assets[self.atype]
        
        self.table.setRowCount(len(self.assets))
        self.table.clearSelection()
        self.entity_widget.unload()

        for i, asset in enumerate(self.assets):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(asset.name))

    def selection_changed(self):
        id = self.table.selectionModel().selectedRows()[0].row()
        self.current_asset = self.assets[id]

        self.entity_widget.reload(self.current_asset)

    def new_asset(self):
        def new_asset_callback(name):
            self.proj.create_asset(self.atype, name)
            self.reload()

        dialog = dialogs.NewAssetDialog(new_asset_callback)
        dialog.exec_()

    def delete_asset(self):
        if not self.current_asset:
            return

        if dcc.confirm_ask('Delete', 'Delete asset "{}"?'.format(self.current_asset.name)):
            self.proj.delete_asset(self.current_asset)

        self.reload()

class EntityWidget(TableWidget):
    def __init__(self, parent=None):
        super(EntityWidget, self).__init__(parent)

        bottom_buttons_layout = QtWidgets.QHBoxLayout()
        self.bottom_buttons_widget = QtWidgets.QWidget()
        self.bottom_buttons_widget.setLayout(bottom_buttons_layout)

        self.open_button = button('Open')
        self.open_button.clicked.connect(lambda: self.current_entity.open())

        self.ref_button = button('Reference')
        self.ref_button.clicked.connect(lambda: self.current_entity.reference())

        self.show_button = button('Show...')
        self.show_button.clicked.connect(lambda: self.current_entity.browse())

        self.versions_button = button('Versions...')
        self.open_button.clicked.connect(lambda: self.current_entity.open())

        self.add_button.clicked.connect(self.new_entity)
        self.remove_button.clicked.connect(self.delete_entity)

        bottom_buttons_layout.addWidget(self.open_button)
        bottom_buttons_layout.addWidget(self.ref_button)
        bottom_buttons_layout.addWidget(self.versions_button)
        bottom_buttons_layout.addWidget(self.show_button)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Pipeline Step', 'Artist', 'Latest Log'])
        self.table.itemSelectionChanged.connect(self.selection_changed)

        self.vertical_layout.addWidget(self.bottom_buttons_widget)
        self.unload()

    def unload(self):
        self.current_entity = None
        self.table.setRowCount(0)

        self.bottom_buttons_widget.setEnabled(False)
        self.button_bar_widget.setEnabled(False)

    def reload(self, asset):
        self.asset = asset

        self.table.setRowCount(len(asset.entities))

        for i, entity in enumerate(asset.entities):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(entity.name))

        self.button_bar_widget.setEnabled(True)
        self.unset_selection()

    def unset_selection(self):
        self.current_entity = None
        self.table.clearSelection()
        self.bottom_buttons_widget.setEnabled(False)

    def selection_changed(self):
        id = self.table.selectionModel().selectedRows()[0].row()
        self.current_entity = self.asset.entities[id]

        self.bottom_buttons_widget.setEnabled(True)

    def new_entity(self):
        all_types = project.ENTITY_TYPES[self.asset.atype]
        types = filter(lambda x: not [x for y in self.asset.entities if x in y.name], all_types)
        
        def new_entity_callback(name):
            self.asset.create_entity(name)
            self.reload(self.asset)

        dialog = dialogs.NewEntityDialog(types, new_entity_callback)
        dialog.exec_()

    def delete_entity(self):
        if not self.current_entity:
            return

        if dcc.confirm_ask('Delete', 'Delete entity "{}"?'.format(self.current_entity.path)):
            self.asset.delete_entity(self.current_entity)

        self.reload(self.asset)