import json
from string import ascii_lowercase
from preprocess import DataExtractor


class Parser:
    """
    Class which using to parse telegram data.
    """
    extractor = DataExtractor("result.json")
    data = extractor.result_data

    def __init__(self):
        self.__chats = []

        self.__messages = []

        self.extract_info()

    def extract_info(self):
        for i in range(len(Parser.data)):
            chat_name = Parser.data[i]['name']
            chat_type = Parser.data[i]['type']
            chat_id = Parser.data[i]['id']
            self.__chats.append((chat_name, chat_type, chat_id))

            tmp_messages = Parser.data[i]['messages']

            tmp_arr = []
            for j in range(len(tmp_messages)):
                sender = tmp_messages[j]['from']
                sender_id = tmp_messages[j]['from_id']
                date, time = tmp_messages[j]['date'].split("T")
                text = tmp_messages[j]['text']
                tmp_arr.append((sender, sender_id, date, time, text))
            self.__messages.append(tmp_arr)

    @property
    def messages(self):
        return self.__messages

    @property
    def chats(self):
        return self.__chats

p = Parser()
