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

        self.__messages_parsed = []

        self.extract_info()

    def extract_info(self):
        messages = []
        for i in range(len(Parser.data)):
            chat_name = Parser.data[i]['name']
            chat_type = Parser.data[i]['type']
            chat_id = Parser.data[i]['id']
            self.__chats.append((chat_name, chat_type, chat_id))

            tmp_messages = Parser.data[i]['messages']
            print(len(tmp_messages))
            for j in range(len(tmp_messages)):
                sender = tmp_messages[j]['from']
                sender_id = tmp_messages[j]['from_id']
                date = tmp_messages[j]['date']
                text = tmp_messages[j]['text']
                messages.append((sender, sender_id, date, text))

        for message in messages:
            message = list(message)
            tmp = message[2].split("T")
            message.remove(message[2])
            message.insert(2, tmp[0])
            message.insert(3, tmp[1])
            self.__messages_parsed.append(message)

    @property
    def messages_parsed(self):
        return self.__messages_parsed

    @property
    def chats(self):
        return self.__chats



