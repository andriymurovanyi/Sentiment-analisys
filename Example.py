# Created by hiddencoder at 25.04.2019

from PyQt5 import QtWidgets, QtGui, QtCore


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.pushButton1 = QtWidgets.QPushButton("Press me")
        self.pushButton1.clicked.connect(self.addCheckbox)
        self.pushButton2 = QtWidgets.QPushButton("OK")
        self.pushButton2.clicked.connect(self.onClicked)

        self.vlayout.addWidget(self.pushButton1)
        self.vlayout.addWidget(self.pushButton2)

        self.checkboxes = []

    def addCheckbox(self):
        checkbox = QtWidgets.QCheckBox()
        self.checkboxes.append(checkbox)
        self.vlayout.addWidget(checkbox)

    def onClicked(self):
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.isChecked():
                print("print {} on the screen".format(i))

if __name__ == '__main__':
    import sys

    application = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setWindowTitle('Hello')
    window.resize(250, 180)
    window.show()
    sys.exit(application.exec_())