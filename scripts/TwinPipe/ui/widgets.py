from TwinPipe.vendor.Qt import QtCore, QtGui, QtCompat, QtWidgets


def button(label):
    btn = QtWidgets.QPushButton(label)
    btn.setMinimumSize(38, 38)

    return btn


class TableWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TableWidget, self).__init__(parent)

        layout = QtWidgets.QHBoxLayout()
        button_bar_layout = QtWidgets.QVBoxLayout()
        button_bar_widget = QtWidgets.QWidget()
        button_bar_widget.setLayout(button_bar_layout)

        self.table = QtWidgets.QTableView()
        self.add_button = button('+')
        self.remove_button = button('-')

        button_bar_layout.addWidget(self.add_button)
        button_bar_layout.addWidget(self.remove_button)
        button_bar_layout.addStretch()

        layout.addWidget(self.table)
        layout.addWidget(button_bar_widget)
        self.setLayout(layout)


class AssetWidget(TableWidget):
    def __init__(self, parent=None):
        super(AssetWidget, self).__init__(parent)


class EntityWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(EntityWidget, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        bottom_buttons_layout = QtWidgets.QHBoxLayout()
        bottom_buttons_widget = QtWidgets.QWidget()
        bottom_buttons_widget.setLayout(bottom_buttons_layout)

        self.open_button = button('Open')
        self.ref_button = button('Reference')
        self.show_button = button('Show')
        self.versions_button = button('Versions...')

        bottom_buttons_layout.addWidget(self.open_button)
        bottom_buttons_layout.addWidget(self.ref_button)
        bottom_buttons_layout.addWidget(self.show_button)
        bottom_buttons_layout.addWidget(self.versions_button)

        self.view = TableWidget()

        layout.addWidget(self.view)
        layout.addWidget(bottom_buttons_widget)

        self.setLayout(layout)
