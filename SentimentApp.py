# Created by hiddencoder at 21.03.2019

import sys

from PyQt5.QtCore import Qt
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel, \
    QVBoxLayout, QHBoxLayout, QScrollArea, QFileDialog, \
    QMessageBox, QCheckBox, QSizePolicy, QSpacerItem, QAction
from Parser import Parser
from preprocess import DataExtractor
from mysql.connector.errors import IntegrityError
from json.decoder import JSONDecodeError
from Model import Analyzer
from dbConnector import Connector


class View(QMainWindow):
    """
    Main view of application
    """

    def __init__(self):
        super(View, self).__init__()

        self.ui = uic.loadUi('interface.ui')
        self.layout = QHBoxLayout()

        self.scrollArea = self.ui.scrollArea
        self.scrollAreaWidgetContents = QWidget()
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.progress = self.ui.progressBar
        self.progress.setVisible(False)
        self.import_action = self.ui.actionImport_3
        self.tabWidget = self.ui.tabWidget
        self.lemmatization_tab = self.ui.textEdit_2
        self.pos_tab = self.ui.textEdit_3

        self.labels = dict()  # Dict of all created labels
        self.parser = Parser()  # Creating parser object
        self._connector = Connector()
        self.lang = ""

        self.chats = []
        self.checks = []
        self.checked = []
        self.messages_to_analyze = []
        self.initUI()

    def initUI(self):
        self.ui.setFixedSize(817, 600)
        self.ui.setWindowTitle('Analyzer')
        self.scrollArea.setWidgetResizable(True)
        self.tabWidget.setTabText(0, "Lemmatization")
        self.tabWidget.setTabText(1, "PoS Tagging")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.import_action.triggered.connect(self.data_import)
        self.ui.clear_button.clicked.connect(self.clear_chosen_messages)
        self.ui.add_button.clicked.connect(self.add_chosen_messages)

        radiobutton1 = self.ui.rus_btn
        radiobutton1.setChecked(True)
        radiobutton1.language = "rus"
        radiobutton1.toggled.connect(self.onClicked)

        radiobutton2 = self.ui.eng_btn
        radiobutton2.language = "eng"
        radiobutton2.toggled.connect(self.onClicked)

        self.ui.analyze_button.clicked.connect(self.analyze)
        self.ui.chats_list.activated[str].connect(self.onActivated)
        self.ui.show()

    def data_import(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getOpenFileName(self, "Choose you're json file",
                                                "json files(*.json)",
                                                options=options)
        if directory[0]:
            file_name = directory[0].split("/")[-1]
            print(directory)
            try:
                extr = DataExtractor(file_name)
            except (ValueError, TypeError):
                self.show_warning("Wrong json format was given!")
            else:
                self.show_chats_list()
                return extr.result_data

    def onActivated(self):
        current_selection = self.ui.chats_list.currentText()
        msg_lst = self._connector.select_messages(current_selection)
        for msg in msg_lst:
            self.chats.append(msg)
        self.deleteItems(self.verticalLayout)
        self.progress.setVisible(True)
        for i in range(len(self.chats) - 1):
            label_name = 'q_label_{}'.format(i)
            check_name = 'q_check_box_{}'.format(i)
            label = QLabel()
            check_box = QCheckBox()
            label.setObjectName(label_name)
            check_box.setObjectName(check_name)
            sender = self.chats[i][0]
            text = self.chats[i][2]
            label.setText("{}: {}".format(sender,
                                          text))
            spaceItem = QSpacerItem(100, 10, QSizePolicy.Expanding)
            label.setWordWrap(True)
            hor_layout = QHBoxLayout()
            hor_layout.addWidget(label)
            hor_layout.addSpacerItem(spaceItem)
            hor_layout.addWidget(check_box)
            hor_layout.setContentsMargins(0, 0, 0, 0)
            check_box.clicked.connect(self.clicked_)
            self.verticalLayout.addLayout(hor_layout, 0)
            self.checks.append(check_box)
            self.labels[label_name] = label
            self.progress.setValue(100 / len(self.chats) * 0.1)

        self.progress.setVisible(False)
        self.chats.clear()

    def show_chats_list(self):
        self.ui.chats_list.addItem("<select chat here>")
        chats = self._connector.select_chats_list()
        for chat in chats:
            self.ui.chats_list.addItem(str(chat[1]))
        self.ui.statusbar.showMessage("Chats added!")

    def clicked_(self):
        checkbox_name = self.sender().objectName()
        checked_label = self.labels["q_label_{}".format(checkbox_name[12:])]
        self.checked.append(checked_label)

    def add_chosen_messages(self):
        print(self.checked)
        for i in self.checked:
            self.ui.choosedEdit.append(i.text())
            text = i.text().split(": ")[1]
            self.messages_to_analyze.append(text)
        self.checked.clear()

    def clear_chosen_messages(self):
        self.ui.choosedEdit.clear()
        self.ui.textEdit_2.clear()
        self.ui.textEdit_3.clear()

    def analyze(self):
        print("Hello")
        analyzer = Analyzer(self.messages_to_analyze, language=self.lang)
        for lemmas in analyzer.lemmatization():
            self.lemmatization_tab.append(str(lemmas))

        for pos in analyzer.pos_tagging():
            self.pos_tab.append(str(pos))

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.lang = radioButton.language
        print(self.lang)

    def deleteItems(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteItems(item.layout())

    def show_warning(self, message):
        warn = QMessageBox.warning(self, 'Message',
                                   message, QMessageBox.Ok)
        return warn

    def noEvent(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = View()

    sys.exit(app.exec())



