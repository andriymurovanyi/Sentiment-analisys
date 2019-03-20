import json
from string import ascii_lowercase
from textblob import TextBlob, Word


def json_read(file_name, encoding='utf-8'):
    """
    Reader.

    Using for JSON-file reading
    :param file_name: file which want to open
    :param encoding: file encoding (utf8 using by default)
    :return: reader_object
    """
    with open(file_name, 'r', encoding=encoding) as file:
        data = json.load(file)
    return data


class Parser:
    """
    Class which using to parse telegram data.
    """
    data = json_read("result.json")

    def __init__(self, chat_id):
        if isinstance(chat_id, int):
            self._chat_id = chat_id
        else:
            raise ValueError("Wrong chat_id type")

        self._all_replicas = []
        self._interlocutor_replicas = []
        self.replicas_split()

    def replicas_split(self):
        """
        Splitter.

        This method using to split all messages by replicas.
        :return: chat replicas mapped to user which send it
        """

        for i in range(len(Parser.data)):
            if Parser.data[i]['id'] == self._chat_id:
                for j in Parser.data[i]['messages']:
                    self._all_replicas.append(j['from'] + ": " + str(j['text']))
                    if j['from_id'] != 354448699:  # User id
                        self._interlocutor_replicas.append(j['text'])
        return

    @staticmethod
    def text_cleaner(text):
        """
        Clean data.

        Method for cleaning punctuation marks, turning all words to lowercase
        :param text: text for cleaning
        :return: cleaned text
        """

        text = text.lower()

        # Ru and Eng alphabet
        en_alpha = ascii_lowercase
        ru_alpha = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

        # Text cleaning
        cleaned_text = ''
        for char in text:
            if (char.isalpha() and (char in ru_alpha or char in en_alpha)) \
                    or (char == ' '):
                cleaned_text += char

        return cleaned_text

    def lemmatisation(self):
        """
        Lemmatisation.

        Word transformation to it's normal form - Lemma
        :param word: word to transform
        :return: Lemma
        """
        lemmas = []

        for replica in self._interlocutor_replicas:
            replica = self.text_cleaner(replica).split()
            for word in replica:
                w = Word(word)
                lemmas.append("(" + word + " --> " + str(w.lemmatize('v')) + ")")
            lemmas.append('\n')

        return ' '.join(lemmas)

    def pos_tagging(self):
        """
        PoS-tagging.

        Method for Part-of-Speech tagging
        :param sentence: Sentence for PoS tagging.
        :return: tags for all words in sentence
        """
        for item in self._interlocutor_replicas:
            sentence = TextBlob(item)
            yield sentence.tags

    @property
    def replicas(self):
        return self._all_replicas

    @property
    def interlocutor_replicas(self):
        return self._interlocutor_replicas


if __name__ == '__main__':
    chat_id = 4685009300  # Eng language chat.


    print('=' * 200)
    print('Replicas splitting started')
    p = Parser(chat_id)
    for rep in p.replicas:
        print(rep)
    print('Replicas splitting finished successfully!')
    print('=' * 200)

    print('Lemmatisation started!')
    print(p.lemmatisation())
    print('=' * 200)

    print("PoS-tagging started!")
    taggs = p.pos_tagging()
    for tag in taggs:
        print(tag)
    print("PoS-tagging completed successfully!")
    print('=' * 200)



