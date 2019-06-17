# Created by hiddencoder at 21.03.2019
import os
import sys
import qrc_rc
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel, \
    QVBoxLayout, QHBoxLayout, QFileDialog, \
    QMessageBox, QCheckBox, QSizePolicy, QSpacerItem, QTableWidgetItem
from Parser import Parser
from preprocess import DataExtractor
from mysql.connector.errors import ProgrammingError
from Model import Analyzer
from database import DataBase


class View(QMainWindow):
    """
    Main view of application
    """

    def __init__(self):
        super(View, self).__init__()

        self.ui: QMainWindow = uic.loadUi('interface.ui', self)
        self.layout = QHBoxLayout()

        self.scrollArea = self.ui.scrollArea
        self.scrollAreaWidgetContents = QWidget()
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.import_action = self.ui.actionImport_3
        self.tabWidget = self.ui.tabWidget
        self.lemmatization_tab = self.ui.textEdit_2
        self.sentiment_tab = self.ui.textEdit_4
        self.pos_tab = self.ui.textEdit_3
        self.table = self.ui.tableWidget

        self.labels = dict()  # Dict of all created labels
        self.parser = Parser()  # Creating parser object
        try:
            self._database = DataBase()
        except ProgrammingError:
            self.show_warning("Some errors with DataBase connection")

        self.chats = []  # All chats with all messages
        self.checks = []  # List of all checkboxes
        self.checked = []  # List of all checked checkboxes
        self.messages_to_analyze = []  #
        self.initUI()

    def initUI(self):
        self.ui.setWindowTitle('Analyzer')
        self.scrollArea.setWidgetResizable(True)
        self.tabWidget.setTabText(0, "Lemmatization")
        self.tabWidget.setTabText(1, "PoS Tagging")
        self.tabWidget.setTabText(2, "Sentiment")

        self.ui.actionExit_5.triggered.connect(self.closeEvent)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.import_action.triggered.connect(self.data_import)
        self.ui.clear_button.clicked.connect(self.clear_chosen_messages)
        self.ui.add_button.clicked.connect(self.add_chosen_messages)

        self.ui.analyze_button.clicked.connect(self.activate_analyze)
        self.ui.chats_list.activated[str].connect(self.render_chats)
        self.ui.show()

    def data_import(self):
        options = QFileDialog.Options()
        options |= QFileDialog.HideNameFilterDetails
        directory = QFileDialog.getOpenFileName(self, "Choose you're json file", os.getcwd(),
                                                "*.json",
                                                options=options)
        if directory[0]:
            file_name = directory[0].split("/")[-1]
            try:
                extr = DataExtractor(file_name)
            except (ValueError, TypeError, KeyError):
                self.show_warning("Wrong json format was given!")
            else:
                self._database.insert_chats_and_messages(self.parser.chats, self.parser.messages)
                self.show_chats_list()
                self.ui.statusbar.showMessage("Chats added!")
                return extr.result_data

    def render_chats(self):
        self.ui.statusbar.showMessage("Wait, please, it may takes a few seconds...")
        self.deleteItems(self.verticalLayout)
        current_selection = self.ui.chats_list.currentText()
        try:
            msg_lst = self._database.select_messages(current_selection)
        except TypeError:
            self.show_warning("You need to choose chat!!")
        else:
            for msg in msg_lst:
                self.chats.append(msg)

            for i in range(len(self.chats)):
                label_name = 'q_label_{}'.format(i)
                check_name = 'q_check_box_{}'.format(i)
                label = QLabel()
                check_box = QCheckBox()
                label.setObjectName(label_name)
                check_box.setObjectName(check_name)
                sender = self.chats[i][0]
                text = self.chats[i][2]
                m_date = self.chats[i][3]
                m_time = self.chats[i][4]
                label.setText("{}: {}\nDate: {}\nTime: {}".format(sender,
                                                                  text, m_date, m_time))
                spaceItem = QSpacerItem(100, 10, QSizePolicy.Expanding)
                label.setWordWrap(True)
                hor_layout = QHBoxLayout()
                hor_layout.addWidget(label)
                hor_layout.addSpacerItem(spaceItem)
                hor_layout.addWidget(check_box)
                hor_layout.setContentsMargins(0, 0, 0, 0)
                check_box.clicked.connect(self.label_clicked)
                self.verticalLayout.addLayout(hor_layout, 0)
                self.checks.append(check_box)
                self.labels[label_name] = label
                QApplication.processEvents()

        self.ui.statusbar.showMessage("Done!")
        self.chats.clear()

    def show_chats_list(self):
        self.ui.chats_list.addItem("<select chat here>")
        chats = self._database.select_chats_list()
        self.ui.chats_list.setMaxCount(len(chats) + 1)
        for chat in chats:
            self.ui.chats_list.addItem(str(chat[1]))

    def label_clicked(self):
        if self.sender().isChecked():
            checkbox_name: QCheckBox = self.sender().objectName()
            checked_label = self.labels["q_label_{}".format(checkbox_name[12:])]
            self.checked.append(checked_label)

    def add_chosen_messages(self):
        self.ui.statusbar.showMessage("Adding message...")
        for i in range(len(self.checked)):
            self.table.setRowCount(len(self.checked))
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["Sentence", "Positive", "Negative", "Neutral", "Official"])
            cell = QTableWidgetItem(self.checked[i].text())
            self.table.setItem(i, 0, cell)
            cell.setFlags(Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable
                          | Qt.ItemIsEnabled)
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

            # self.checked[i] = self.checked[i].text().split(":")
            text: str = self.checked[i].text()
            message, date, time = text[text.find(":") + 2:].split("\n")
            self.messages_to_analyze.append((message, date, time))
        for checkbox in self.checks:
            checkbox.setChecked(False)
        self.ui.statusbar.showMessage("Done!")
        self.activate_insert()
        self.checked.clear()

    def clear_chosen_messages(self):
        self.checked.clear()
        self.table.clear()
        self.lemmatization_tab.clear()
        self.pos_tab.clear()
        self.sentiment_tab.clear()
        self.messages_to_analyze.clear()

    def activate_analyze(self):
        messages_text_to_analyze = [i[0] for i in self.messages_to_analyze]
        # Selecting words and lemmas from DB after inserting or updating
        selected_lemmas = [self._database.select_lemmatization(i) for i in messages_text_to_analyze]

        # Selecting words and pos_tags from DB after inserting or updating
        selected_pos_tags = [self._database.select_pos_tagging(i) for i in messages_text_to_analyze]
        for i in messages_text_to_analyze:
            for items in selected_lemmas:
                for item in items:
                    self.lemmatization_tab.append("[w] word: {}; "
                                                  "[le] lemma: {}.".format(item[0], item[1]))
            self.lemmatization_tab.append("\n")
            break

        for i in messages_text_to_analyze:
            for items in selected_pos_tags:
                for item in items:
                    self.pos_tab.append("[w] word: {}; "
                                        "[pos] pos-tag: {} ({})".format(item[0], item[1],
                                                                        Analyzer.get_pos_description(
                                                                            item[1])))
            self.pos_tab.append("\n")
            break

        sentiments = Analyzer.sentiment(messages_text_to_analyze)
        for item in sentiments:
            self.sentiment_tab.append("[S] Sentence: {};\n *"
                                      "[pol] polarity: {};\n *[sub] subjectivity: {}"
                                      .format(item[0], item[1].polarity, item[1].subjectivity))

    def activate_insert(self):
        messages_text_to_analyze = [i[0] for i in self.messages_to_analyze]  # Text of messages which were selected
        try:
            analyzer = Analyzer(messages_text_to_analyze,
                                language=Analyzer.detect_language(messages_text_to_analyze[0]))
        except IndexError:
            self.show_warning("No messages yet!")
        else:
            #  Going to insert words to DB
            for message in self.messages_to_analyze:
                print(" [T] Tokenization '{}'".format(analyzer.tokenization(message[0])))
                self._database.insert_words(message, analyzer)
            results = Analyzer.sentiment(messages_text_to_analyze)
            for i in range(len(self.messages_to_analyze)):
                self._database.insert_results(self.messages_to_analyze[i], results[i])

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

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def noEvent(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.processEvents()
    view = View()

    sys.exit(app.exec())
