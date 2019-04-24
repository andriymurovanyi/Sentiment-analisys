# Created by hiddencoder at 21.03.2019

import sys

from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel, \
    QVBoxLayout, QHBoxLayout, QScrollArea, QFileDialog, QMessageBox, QCheckBox, QSizePolicy, QSpacerItem
from Parser import Parser
from preprocess import DataExtractor
from json.decoder import JSONDecodeError
from dbConnector import Connector


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
        self.chats = []
        self.checks = []

        self._connector = Connector()

        self.initUI()

    def initUI(self):

        self.ui.setFixedSize(817, 600)

        self.ui.setWindowTitle('Analyzer')

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.ui.import_button.clicked.connect(self.data_import)
        self.show_chat_list()
        self.ui.chats_list.activated[str].connect(self.onActivated)

        self.ui.show()

    def data_import(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getOpenFileName(self, "Choose you're json file", "json files(*.json)", options=options)
        if directory[0]:
            file_name = directory[0].split("/")[-1]
            print(directory)
            try:
                extr = DataExtractor(file_name)
            except (ValueError, IndexError):
                warn = QMessageBox.warning(self, 'Message',
                                             "Wrong json format were gived!", QMessageBox.Ok)
            else:
                return extr.result_data

    def onActivated(self):
        current_selection = self.ui.chats_list.currentText()
        select_id_ch = "SELECT idChat from chat where chat_name = '{}'".format(str(current_selection))
        self._connector.cursor.execute(select_id_ch)
        id_ch = self._connector.cursor.fetchone()[0]


        select_messages = "SELECT sender, sender_id, text from message where idChat = {}".format(id_ch)
        self._connector.cursor.execute(select_messages)
        msg_lst = self._connector.cursor.fetchall()
        for msg in msg_lst:
            self.chats.append(msg)

        self.deleteItems(self.verticalLayout)

        for i in range(len(self.chats) - 1):
            name = 'q_label_{}'.format(i)
            label = QLabel()
            check_box = QCheckBox()
            label.setObjectName(name)
            label.setText("{}: {}".format(self.chats[i][0], self.chats[i][2]))

            # if self.chats[i][0] == self.chats[i + 1][0]:
            #     label.setStyleSheet("background-color: rgb(194, 197, 255);")
            # Set background color depending on who wrote message.
            spaceItem = QSpacerItem(100, 10, QSizePolicy.Expanding)
            label.setWordWrap(True)
            hor_layout = QHBoxLayout()
            hor_layout.addWidget(label)
            hor_layout.addSpacerItem(spaceItem)
            hor_layout.addWidget(check_box)
            hor_layout.setContentsMargins(0, 0, 0, 0)
            check_box.stateChanged.connect(self.item_checked)
            self.verticalLayout.addLayout(hor_layout, 0)
            self.checks.append(check_box)
            self.labels[name] = label
        self.chats.clear()

    def item_checked(self, state):

        if state == Qt.Checked:
            print("Checked!")

        else:
            print("Unchecked!")

    def show_chat_list(self):
        self.ui.chats_list.addItems(["<choose chat here>"])
        select_chats = "SELECT * FROM chat"
        self._connector.cursor.execute(select_chats)
        records = self._connector.cursor.fetchall()
        for i in records:
            self.ui.chats_list.addItem(i[1])

    def deleteItems(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteItems(item.layout())

    def noEvent(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = View()

    sys.exit(app.exec())



