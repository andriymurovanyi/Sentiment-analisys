# Created by hiddencoder at 23.04.2019

from nltk import word_tokenize, pos_tag, chunk
from nltk.stem import WordNetLemmatizer
from dbConnector import Connector
from Parser import Parser
from string import ascii_lowercase
from textblob import TextBlob
import pymorphy2


class Analyzer:
    """
    Class which contains main app logic.
    """

    def __init__(self, user_id=354448699, chat_id=4685009300):
        if isinstance(chat_id, int) and isinstance(user_id, int):
            self._chat_id = chat_id
            self._user_id = user_id
        else:
            raise ValueError("Wrong chat_id type given")
        self._connector = Connector()
        # self.replicas_split()
        self._all_replicas = []
        self._interlocutor_replicas = []

    def db_filling(self, *args):
        chats = list(args[0])
        messages = list(args[1])
        sql_chats = "INSERT INTO chat (chat_name, chat_type, chat_id) VALUES (%s, %s, %s)"
        self._connector.cursor.executemany(sql_chats, chats)
        self._connector.cnx.commit()
        print(self._connector.cursor.lastrowid)
        for i in messages:
            select_chat_id = "select idChat from chat where chat_id = {}".format(i[2])
            self._connector.cursor.execute(select_chat_id)
            if self._connector.cursor.fetchone():
                id_ch = self._connector.cursor.fetchall()[0][0]

                # TODO This function !!! Today !
                counter = 0
                print(id_ch)
                sql_messages = "INSERT INTO message (sender, sender_id, " \
                               "m_date, m_time, text, idChat) VALUES (%s, %s, %s, %s, %s, %s)"

                self._connector.cursor.execute(sql_messages, i + [id_ch])
                counter += 1

        self._connector.cnx.commit()
        self._connector.cursor.close()
        self._connector.cnx.close()


    # def replicas_split(self):
    #     """
    #     Splitter.
    #
    #     This method using to split all messages by replicas.
    #     :return: chat replicas mapped to user which send it
    #     """
    #
    #     for i in range(len(Parser.data)):
    #         if Parser.data[i]['id'] == self._chat_id:
    #             print(Parser.data[i]["id"])
    #             for j in Parser.data[i]['messages']:
    #                 self._all_replicas.append(j['from'] + ": " + str(j['text']))
    #                 if j['from_id'] != self._user_id:  # User id
    #                     self._interlocutor_replicas.append(j['text'])
    #     return

    # @staticmethod
    # def text_cleaner(text):
    #     """
    #     Clean data.
    #
    #     Method for cleaning punctuation marks, turning all words to lowercase
    #     :param text: text for cleaning
    #     :return: cleaned text
    #     """
    #
    #     text = text.lower()
    #
    #     # Ru and Eng alphabet
    #     en_alpha = ascii_lowercase
    #     ru_alpha = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    #
    #     # Text cleaning
    #     cleaned_text = ''
    #     for char in text:
    #         if (char.isalpha() and (char in ru_alpha or char in en_alpha)) \
    #                 or (char == ' '):
    #             cleaned_text += char
    #
    #     return cleaned_text
    #
    # @staticmethod
    # def tokenization(sentence):
    #     """
    #     Tokenizer.
    #
    #     Choose words from sentence
    #     :return:
    #     """
    #     tokens = word_tokenize(sentence)
    #     return tokens
    #
    # def lemmatization(self):
    #     """
    #     Lemmatization.
    #
    #     Word transformation to it's normal form - Lemma
    #     :return: Lemmas list
    #     """
    #     lemmas = []
    #     lemmatizer = WordNetLemmatizer()
    #
    #     for replica in self._interlocutor_replicas:
    #         replica = self.text_cleaner(replica).split()
    #         for word in replica:
    #             lemmas.append("(" + word + " --> " + lemmatizer.lemmatize(word, pos="v") + ")")
    #         lemmas.append('\n')
    #
    #     return lemmas
    #
    # def pos_tagging(self, language='eng'):
    #     """
    #     PoS-tagging.
    #
    #     Method for Part-of-Speech tagging
    #     :return: tags for all words in sentence
    #     """
    #     tagged = []
    #     print(self._interlocutor_replicas)
    #     for item in self._interlocutor_replicas:
    #         tagged.append(pos_tag(word_tokenize(item), lang=language))
    #     return tagged
    #
    # def gramatical_categories(self):
    #     pass
    #
    # @property
    # def replicas(self):
    #     return self._all_replicas
    #
    # @property
    # def interlocutor_replicas(self):
    #     return self._interlocutor_replicas

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, new_user_id):
        assert isinstance(new_user_id, int), 'Wrong type given'
        self._user_id = new_user_id

    @property
    def chat_id(self):
        return self._chat_id

    @chat_id.setter
    def chat_id(self, new_chat_id):
        assert isinstance(new_chat_id, int), 'Wrong type given'
        self._chat_id = new_chat_id


if __name__ == '__main__':
    print('=' * 200)
    print('Replicas splitting started')
    analyzer = Analyzer(chat_id=4855961349)
    parser = Parser()
    analyzer.db_filling(parser.chats, parser.messages_parsed)


    # print('Lemmatization started!')
    # print(' '.join(p.lemmatization()))
    #
    # print('Lemmatization completed successfully!')
    # print('=' * 200)
    #
    # print("PoS-tagging started!")
    # tags = p.pos_tagging(language='rus')
    # for tag in tags:
    #     print(tag)
    # print("PoS-tagging completed successfully!")
    # print('=' * 200)

    #
    # for replica in p.interlocutor_replicas:
    #     print("------")
    #     print("Replica: {};\nPolarity: {} ".format(replica, p.result(replica)))
    #     print("------")

    # new_data = json_read('PoS_description.json')
    # for i in range(len(new_data)):
    #     print("================================================================")
    #     print("||" + new_data[i]['tag'] + " <--> " + new_data[i]['description'] + "||")
    #     print('----------------------------------------------------------------')

    # TODO 1) Личное отношение / безличное
    # TODO 2) Официальное / не официальное
    # TODO 3) Доброжелательное или нет
    # TODO 4) Позитивное негативное отношение к собеседнику(!).
    # TODO 5) Уважительное / не уважительное
    # TODO 6) ... !!!
