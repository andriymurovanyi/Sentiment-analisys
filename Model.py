# Created by hiddencoder at 23.04.2019
import json
import string
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import pymorphy2


class Analyzer:
    """
    Class which contains main app logic.
    """

    def __init__(self, replicas, language="eng"):
        if isinstance(replicas, list) or isinstance(replicas, str):
            self.__language = language
            self.__replicas = replicas
        else:
            raise ValueError("Wrong data type was given")

    @staticmethod
    def tokenization(sentence):
        """
        Tokenizer.

        Choose words from sentence
        :return:
        """
        tokens = word_tokenize(sentence)
        tokens = [i.lower() for i in tokens if i not in string.punctuation]
        return tokens

    def lemmatize_word(self, word):
        if self.__language == "eng":
            return WordNetLemmatizer().lemmatize(word, pos="v")
        else:
            morph = pymorphy2.MorphAnalyzer()
            p = morph.parse(word)[0]
            return p.normal_form

    def pos_tag_sentence(self, sentence):
        """
        PoS-tagging.

        Method for Part-of-Speech tagging
        :return: tags for all words in sentence
        """
        if self.__language == "eng":
            return pos_tag(self.tokenization(sentence))
        elif self.__language == "rus":
            morph = pymorphy2.MorphAnalyzer()
            return list(map(lambda x: tuple([x, morph.parse(x)[0].tag.POS]),
                            self.tokenization(sentence)))

    @staticmethod
    def sentiment(sentences):
        sentiments = []
        for item in sentences:
            blob = TextBlob(item)
            sentiments.append((item, blob.sentiment))
        return sentiments

    @staticmethod
    def get_pos_description(tag):
        with open("PoS_description.json", 'r', encoding="utf-8")as file:
            data = json.load(file)
        tag_description = data["tags"][tag]
        return tag_description

    @staticmethod
    def detect_language(sentence):
        """
        Language detecting.

        Used to detect language of sentence
        :param sentence: string sentence
        :return: language
        """
        result = TextBlob(sentence).detect_language()
        if result == "ru":
            result += "s"
        elif result == "en":
            result += "g"
        return result

    @property
    def language(self):
        return self.__language
