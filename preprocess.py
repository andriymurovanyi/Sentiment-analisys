# Created by hiddencoder at 23.04.2019
import json


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
            json.dump(list_to_insert, file)

    def __get_data(self):
        with open("data.json", "r", encoding=self.__encoding) as file:
            data = json.load(file)
        return data

    @property
    def result_data(self):
        return self.__result_data


