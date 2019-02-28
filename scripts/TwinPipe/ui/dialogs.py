from TwinPipe.vendor.Qt import QtCore, QtGui, QtCompat, QtWidgets
import TwinPipe.maya_interop as dcc

def is_valid_name(name):
    import string

    valid_set = string.ascii_letters + '-'
    for char in name:
        if char not in valid_set:
            return False

    return True

class NewAssetDialog(QtWidgets.QDialog):
    def __init__(self, callback, parent=None):
        super(NewAssetDialog, self).__init__(parent)

        self.callback = callback

        layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()
        button_layout_widget = QtWidgets.QWidget()
        button_layout_widget.setLayout(button_layout)

        self.label = QtWidgets.QLabel("Create a new asset named: ")
        self.name = QtWidgets.QLineEdit()
        self.name.returnPressed.connect(self.confirm_input)

        self.ok = QtWidgets.QPushButton('Create')
        self.ok.clicked.connect(self.confirm_input)

        self.cancel = QtWidgets.QPushButton('Cancel')
        self.cancel.clicked.connect(self.reject)

        layout.addWidget(self.label)
        layout.addWidget(self.name)
        button_layout.addWidget(self.ok)
        button_layout.addWidget(self.cancel)
        layout.addWidget(button_layout_widget)

        self.setLayout(layout)

    def confirm_input(self):
        text = self.label.text()

        if not is_valid_name(text):
            dcc.error_message('Invalid name, you cannot have spaces or special characters other than "-"')

        self.callback(text)
