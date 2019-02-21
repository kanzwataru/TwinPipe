from TwinPipe.vendor.Qt import QtCore, QtGui, QtCompat, QtWidgets


def button(label):
    btn = QtWidgets.QPushButton(label)
    btn.setMinimumSize(38, 38)

    return btn


class TableWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout()
        self.button_bar_layout = QtWidgets.QVBoxLayout()
        button_bar_widget = QtWidgets.QWidget()
        button_bar_widget.setLayout(self.button_bar_layout)

        self.vertical_layout = QtWidgets.QVBoxLayout()
        vertical_widget = QtWidgets.QWidget()
        vertical_widget.setLayout(self.vertical_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.horizontalHeader().setStretchLastSection(True)
        self.vertical_layout.addWidget(self.table)

        self.add_button = button('+')
        self.remove_button = button('-')
        self.button_bar_layout.addWidget(self.add_button)
        self.button_bar_layout.addWidget(self.remove_button)
        self.button_bar_layout.addStretch()

        layout.addWidget(vertical_widget)
        layout.addWidget(button_bar_widget)
        self.setLayout(layout)


class AssetWidget(TableWidget):
    def __init__(self, parent=None):
        super(AssetWidget, self).__init__(parent)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Name', 'Status', 'Latest Log'])


class EntityWidget(TableWidget):
    def __init__(self, parent=None):
        super(EntityWidget, self).__init__(parent)

        bottom_buttons_layout = QtWidgets.QHBoxLayout()
        bottom_buttons_widget = QtWidgets.QWidget()
        bottom_buttons_widget.setLayout(bottom_buttons_layout)

        self.open_button = button('Open')
        self.ref_button = button('Reference')
        self.show_button = button('Show...')
        self.versions_button = button('Versions...')

        bottom_buttons_layout.addWidget(self.open_button)
        bottom_buttons_layout.addWidget(self.ref_button)
        bottom_buttons_layout.addWidget(self.versions_button)
        bottom_buttons_layout.addWidget(self.show_button)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Pipeline Step', 'Artist', 'Latest Log'])

        self.vertical_layout.addWidget(bottom_buttons_widget)
