from TwinPipe.vendor.Qt import QtCore, QtGui, QtCompat, QtWidgets
import TwinPipe.maya_interop as dcc

def is_valid_name(name):
    import string

    valid_set = string.ascii_letters + string.digits + '-'
    print valid_set
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

        self.setWindowTitle("Asset Creation")
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
        text = self.name.text()

        if not is_valid_name(text):
            dcc.error_message('Invalid name, you cannot have spaces or special characters other than "-"')
            return

        self.callback(text)
        self.close()


class NewEntityDialog(QtWidgets.QDialog):
	def __init__(self, choices, callback, parent=None):
		super(NewEntityDialog, self).__init__(parent)
		
        layout = QtWidgets.QVBoxLayout()
        combo_layout = QtWidgets.QHBoxLayout()
        combo_layout_widget = QtWidgets.QWidget()
        combo_layout_widget.setLayout(combo_layout)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout_widget = QtWidgets.QWidget()
        button_layout_widget.setLayout(button_layout)
		
		self.setWindowTitle("Maya File Creation")
		self.label = QtWidgets.QLabel("Create a new Maya file")
		self.combo_label = QtWidgets.QLabel("Pipeline stage: ")
		self.stage = QtWidgets.QComboBox()
		
		for choice in choices:
			self.stage.addItem(choice)
		self.stage.addItem("Custom...")
		self.stage.setCurrentIndex(0)

		self.custom = QtWidgets.QLineEdit()
		
		self.ok = QtWidgets.QPushButton('Create')
        self.ok.clicked.connect(self.confirm_input)

        self.cancel = QtWidgets.QPushButton('Cancel')
        self.cancel.clicked.connect(self.reject)
		
		combo_layout.addWidget(self.combo_label, self.stage)
        button_layout.addWidget(self.ok)
        button_layout.addWidget(self.cancel)
        layout.addWidget(button_layout_widget)
		layout.addWidget(combo_layout_widget)

		self.setLayout(layout)
