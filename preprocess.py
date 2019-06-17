# Created by hiddencoder at 23.04.2019
import json
import re
import emoji


def give_emoji_free_text(dict_):
    text = dict_['text'].encode()
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if
                           not any(i in str for i in emoji_list)])
    dict_['text'] = clean_text + " "
    return dict_

class DataExtractor:
    """
    Class which allows to extract data.
    """

    def __init__(self, file, encoding="utf-8-sig"):
        self.__file = file
        self.__encoding = encoding
        self.__json_dump()
        self.__result_data = self.__get_data()

    def __json_read(self):
        """
        Reader.

        Using for JSON-file reading
        :param file_name: file which want to open
        :param encoding: file encoding (utf8 using by default)
        :return: reader_object
        """
        with open(self.__file, 'r', encoding=self.__encoding) as file:

            data = json.load(file)
            if data['chats']['list']:
                list_to_insert = data['chats']['list']
            else:
                raise ValueError

        return list_to_insert

    def __json_dump(self):
        with open("data.json", 'w', encoding=self.__encoding) as file:
            list_to_insert = self.__json_read()
            for i in range(len(list_to_insert)):
                tmp_messages = list_to_insert[i]['messages']
                tmp_messages = list(filter(lambda x: not isinstance(x["text"], list), tmp_messages))
                list_to_insert[i]['messages'] = tmp_messages
            # for i in list_to_insert: print(i)
            for i in list_to_insert:
                i['messages'] = list(map(lambda x: give_emoji_free_text(x), i["messages"]))
            json.dump(list_to_insert, file)

    def __get_data(self):
        with open("data.json", "r", encoding=self.__encoding) as file:
            data = json.load(file)
        return data

    @property
    def file(self):
        return self.__file

    @property
    def result_data(self):
        return self.__result_data
