import mysql.connector


class Connector:
    """
    Connection to database and manipulations.
    """

    def __init__(self):
        self.__cnx = mysql.connector.connect(user="root", password="123456",
                                             host="localhost", database="sentimentmodel")
        self.__cursor = self.__cnx.cursor()

    def db_filling(self, *args):
        """
        Database filling.

        This method using for adding data to database
        :param args: data which we want to add
        """
        chats = list(args[0])
        messages = list(args[1])
        sql_chats = "INSERT INTO chat (chat_name, chat_type, chat_id) " \
                    "VALUES (%s, %s, %s)"
        self.__cursor.executemany(sql_chats, chats)
        self.__cnx.commit()
        for i in range(len(chats)):
            select_chat_id = "select idChat from chat where chat_id = {}".format(chats[i][2])
            self.__cursor.execute(select_chat_id)
            id_ch = self.__cursor.fetchone()[0]
            messages[i] = list(map(lambda x: list(x) + [id_ch], messages[i]))
            sql_messages = "INSERT INTO message (sender, sender_id, " \
                           "m_date, m_time, text, idChat) VALUES (%s, %s, %s, %s, %s, %s)"
            self.__cursor.executemany(sql_messages, messages[i])
        self.__cnx.commit()
        self.__cursor.close()
        self.__cnx.close()

    def select_chats_list(self):
        """
        Chats selection.

        All available chats selection
        :return: all records with chats
        """
        select_chats = "SELECT * FROM chat"
        self.__cursor.execute(select_chats)
        records = self.__cursor.fetchall()
        self.__cursor.close()
        self.__cnx.close()
        return records

    def select_messages(self, current_selection):
        """
        Messages selection.

        Select all messages for chat which was chosen.
        :param current_selection: current chat.
        :return: list of all messages for current chat.
        """
        select_id_ch = "SELECT idChat from chat where chat_name = " \
                       "'{}'".format(str(current_selection))
        self.__cursor.execute(select_id_ch)
        id_ch = self.__cursor.fetchone()[0]

        select_messages = "SELECT sender, sender_id, " \
                          "text from message where idChat = {}".format(id_ch)
        self.__cursor.execute(select_messages)
        msg_lst = self.__cursor.fetchall()
        self.__cursor.close()
        self.__cnx.close()
        return msg_lst

    @property
    def cnx(self):
        return self.__cnx

    @property
    def cursor(self):
        return self.__cursor
