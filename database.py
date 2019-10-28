from dbConnector import Connector
import mysql.connector

# ==================================================== SQL QUERIES =====================================================


SQL_SELECT_CHAT = "SELECT * FROM chat WHERE chat_id = %s"  # Check if chat already exist
SQL_SELECT_CHATS = "SELECT * FROM chat"  # Select all chats to display them
SQL_INSERT_CHATS = "INSERT INTO chat (chat_name, chat_type, chat_id) VALUES (%s, %s, %s)"  # Chats inserting
SQL_SELECT_CHAT_ID = "SELECT idChat FROM chat WHERE chat_id = %s"

SQL_CHECK_MESSAGE = "SELECT * FROM message WHERE idChat=%s"  # Check if message already exist
SQL_INSERT_MESSAGES = "INSERT INTO message (sender, sender_id, m_date, m_time, text, idChat) " \
               "VALUES (%s, %s, %s, %s, %s, %s)"  # Messages inserting


SQL_SELECT_MESSAGES = "SELECT sender, sender_id,text, m_date, m_time " \
                      "FROM message WHERE idChat = " \
                      "(SELECT idChat from chat where chat_name = %s)"  # Select all messages for current selected chat.

SQL_SELECT_MESSAGE_ID = "SELECT idMessage FROM message " \
                        "WHERE text = %s AND m_date = %s AND m_time = %s"  # Select message id.

SQL_SELECT_WORD = "SELECT * FROM word WHERE word_text = %s AND lemma = %s"  # Check if word already exist
SQL_SELECT_WORD_ID = "SELECT idWord FROM word WHERE word_text = %s AND lemma = %s"  # Select all words id's
SQL_INSERT_WORD = "INSERT INTO word (word_text, lemma) VALUES (%s, %s)"
SQL_INSERT_MESSAGE_AND_WORD = "INSERT INTO message_and_word (idMessage, idWord, pos_tag, position) " \
                            "VALUES (%s, %s, %s, %s)"

SQL_SELECT_LEMMATIZATION = "SELECT DISTINCT word_text, lemma " \
                           "FROM word INNER JOIN message_and_word maw ON word.idWord = maw.idWord" \
                           " INNER JOIN message m ON maw.idMessage = m.idMessage " \
                           "WHERE m.text = %s ORDER BY maw.position"  # Select lemmatization results from DataBase

SQL_SELECT_POS_TAGGING = "SELECT DISTINCT word_text, pos_tag " \
                           "FROM word INNER JOIN message_and_word maw ON word.idWord = maw.idWord" \
                           " INNER JOIN message m ON maw.idMessage = m.idMessage " \
                           "WHERE m.text = %s ORDER BY maw.position"  # Select PoS-tagging results from DataBase


SQL_INSERT_RESULTS = "INSERT INTO result(polarity, subjectivity, idMessage) VALUES (%s, %s, %s)"  # Results inserting
SQL_SELECT_RESULTS = "SELECT text, polarity, subjectivity " \
                     "FROM message " \
                     "INNER JOIN result ON result.idMessage = message.idMessage " \
                     "WHERE message.text = %s"  # Select all results by message
# ======================================================================================================================


class DataBase:
    """
    DataBase and manipulations.
    """
    def __init__(self):
        self.__connector = Connector()
        self.__cursor = self.__connector.cursor
        self.__cnx = self.__connector.cnx

    def _is_chat(self, chat_id):
        """
        Existing.

        Check if chat already exist in DataBase
        :param chat_id: id for chat
        :return: True if exist else - False
        """

        self.__cursor.execute(SQL_SELECT_CHAT, (chat_id,))
        if self.__cursor.fetchall():
            return True
        else:
            return False

    def _is_message(self, chat_id):
        """
        Existing.

        Check if message already in DataBase
        :return: True if exist else - False
        """

        self.__cursor.execute(SQL_CHECK_MESSAGE, (chat_id,))
        if self.__cursor.fetchall():
            return True
        else:
            return False

    def _is_word(self, word_text, lemma):
        """
        Existing.

        Check if word already exist in DataBase.
        :param word_text: word text
        :param lemma: word normal form
        :return: True if exist else - False
        """

        self.__cursor.execute(SQL_SELECT_WORD, (word_text, lemma))
        if self.__cursor.fetchall():
            return True
        else:
            return False

    def _is_result(self, idMessage):
        sql_query = "SELECT idMessage FROM result WHERE idMessage = %s"
        self.__cursor.execute(sql_query, (idMessage, ))
        if self.__cursor.fetchall():
            return True
        else:
            return False

    def insert_chats_and_messages(self, *args):
        """
        Database filling.

        This method using for adding data to database
        :param args: data which we want to add
        """
        chats = list(args[0])
        messages = list(args[1])
        for i in range(len(chats)):
            if not self._is_chat(chats[i][2]):
                self.__cursor.execute(SQL_INSERT_CHATS, chats[i])
                self.__cnx.commit()
        for i in range(len(chats)):
            self.__cursor.execute(SQL_SELECT_CHAT_ID, (chats[i][2], ))
            id_ch = self.__cursor.fetchone()[0]
            print(messages)
            messages[i] = list(map(lambda x: list(x) + [id_ch], messages[i]))
            if not self._is_message(id_ch):
                self.__cursor.executemany(SQL_INSERT_MESSAGES, messages[i])
                self.__cnx.commit()

    def select_chats_list(self):
        """
        Chats selection.

        All available chats selection
        :return: all records with chats
        """
        self.__cursor.execute(SQL_SELECT_CHATS)
        records = self.__cursor.fetchall()
        return records

    def select_messages(self, current_selection):
        """
        Messages selection.

        Select all messages for chat which was chosen.
        :param current_selection: current chat.
        :return: list of all messages for current chat.
        """
        self.__cursor.execute(SQL_SELECT_MESSAGES, (current_selection, ))
        msg_lst = self.__cursor.fetchall()
        print(" [M] Message list '{}'".format(msg_lst))
        return msg_lst

    def select_words_id(self, word_text, lemma):
        self.__cursor.execute(SQL_SELECT_WORD_ID, (word_text, lemma))
        return self.__cursor.fetchall()[0][0]

    def select_lemmatization(self, text):
        self.__cursor.execute(SQL_SELECT_LEMMATIZATION, (text,))
        return self.__cursor.fetchall()

    def select_pos_tagging(self, text):
        self.__cursor.execute(SQL_SELECT_POS_TAGGING, (text,))
        return self.__cursor.fetchall()

    def select_results(self, text):
        self.__cursor.execute(SQL_SELECT_RESULTS, (text, ))
        return self.__cursor.fetchall()[0][0]

    def insert_words(self, message: tuple, analyzer):
        date_time = [message[i][6:] for i in range(1, len(message))]
        message = [message[0], date_time[0], date_time[1]]
        self.__cursor.execute(SQL_SELECT_MESSAGE_ID, message)
        idMessage = self.__cursor.fetchall()
        words = analyzer.tokenization(message[0])
        lemmas = [analyzer.lemmatize_word(i) for i in words]
        idWords = []
        for i in range(len(words)):
            if not self._is_word(words[i], lemmas[i]):
                self.__cursor.execute(SQL_INSERT_WORD, (words[i], lemmas[i]))
                self.__cnx.commit()
            idWords.append(self.select_words_id(words[i], lemmas[i]))
        pos_tags = analyzer.pos_tag_sentence(message[0])
        for i in range(len(words)):
            positions = [j for j, x in enumerate(words) if x == words[i]]
            for p in positions:
                self.__cursor.execute(SQL_INSERT_MESSAGE_AND_WORD,
                                      (idMessage[0][0], idWords[i],
                                       str(pos_tags[i][1]), p))
                self.__cnx.commit()

    def insert_results(self, message, result):
        date_time = [message[i][6:] for i in range(1, len(message))]
        message = [message[0], date_time[0], date_time[1]]
        self.__cursor.execute(SQL_SELECT_MESSAGE_ID, message)
        idMessage = self.__cursor.fetchall()[0][0]
        polarity = round(result[1].polarity, 3)
        subjectivity = round(result[1].subjectivity)
        if not self._is_result(idMessage):
            self.__cursor.execute(SQL_INSERT_RESULTS, (polarity, subjectivity, idMessage))
            self.__cnx.commit()

