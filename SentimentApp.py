# Created by hiddencoder at 21.03.2019

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea
from Parser import Parser


class View(QMainWindow):
    """
    Main view of application
    """

    def __init__(self):
        super(View, self).__init__()
        self.ui = uic.loadUi('interface.ui')
        self.layout = QHBoxLayout()
        self.parser = Parser()  # Creating parser object

        self.scrollArea = self.ui.scrollArea
        self.scrollAreaWidgetContents = QWidget()
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.labels = dict()  # Dict of all created labels

        self.user_id_field = self.ui.user_id_field
        self.chat_id_field = self.ui.chat_id_field
        self.submit_button = self.ui.submit_button

        self.initUI()

    def initUI(self):

        self.ui.setFixedSize(817, 600)
        self.ui.setWindowTitle('Analyzer')

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.layout.addWidget(self.scrollArea)
        self.user_id_field.setText(str(self.parser.user_id))
        self.user_id_field.setEnabled(False)  # TODO <Something with user id field>
        self.chat_id_field.setText(str(self.parser.chat_id))
        self.submit_button.clicked.connect(self.load_preview)

        self.ui.show()

    def load_preview(self):
        # TODO <Data type checking>
        self.parser.user_id = int(self.user_id_field.text())
        self.parser.chat_id = int(self.chat_id_field.text())

        # Clean area before filling.
        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().setParent(None)

        for i in range(len(self.parser.data)):
            name = 'q_label_{}'.format(i)
            if self.parser.data[i]['id'] == self.parser.chat_id:
                for message in self.parser.data[i]['messages']:
                    label = QLabel()
                    label.setObjectName(name)
                    label.setText("{}: {}".format(message['from'], message['text']))

                    # Set background color depending on who wrote message.
                    if message['from_id'] != self.parser.user_id:
                        label.setStyleSheet("QLabel { background-color : #13ff36 ;"
                                            "font: 75 12pt 'Times New Roman'}")
                    else:
                        label.setStyleSheet("QLabel { background-color : #1048ff ;"
                                            "font: 75 12pt 'Times New Roman'}")
                    label.setWordWrap(True)
                    self.verticalLayout.addWidget(label, 0)
                    self.labels[name] = label

    def noEvent(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = View()

    sys.exit(app.exec())



