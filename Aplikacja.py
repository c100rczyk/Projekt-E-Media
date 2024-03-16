from PySide6 import QtCore, QtWidgets, QtGui
import sys
import random

class PNG_APP(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.button = QtWidgets.QPushButton("Button")
        self.text = QtWidgets.QLabel("Hello world!!!")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    def magic(self):
        self.text.setText(random.choice(self.hello))

app = QtWidgets.QApplication([])
widget = PNG_APP()
widget.resize(800,500)
widget.show()

sys.exit(app.exec())

