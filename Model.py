# Created by hiddencoder at 23.04.2019

from nltk import word_tokenize, pos_tag, chunk
from nltk.stem import WordNetLemmatizer

from Parser import Parser
from string import ascii_lowercase
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

    @staticmethod
    def tokenization(sentence):
        """
        Tokenizer.

        Choose words from sentence
        :return:
        """
        tokens = word_tokenize(sentence)
        return tokens

    def lemmatization(self):
        """
        Lemmatization.

        Word transformation to it's normal form - Lemma
        :return: Lemmas list
        """
        lemmas = []

        if self.__language == "eng":
            lemmatizer = WordNetLemmatizer()
            for replica in self.__replicas:
                replica = self.text_cleaner(replica).split()
                for word in replica:
                    lemmas.append("(" + word + " --> " + lemmatizer.lemmatize(word, pos="v") + ")")
                lemmas.append('\n')
        elif self.__language == "rus":
            morph = pymorphy2.MorphAnalyzer()
            for replica in self.__replicas:
                r = replica.split()
                for word in r:
                    p = morph.parse(word)[0]
                    lemmas.append("(" + word + " --> " + p.normal_form + ")")


        return lemmas

    def pos_tagging(self):
        """
        PoS-tagging.

        Method for Part-of-Speech tagging
        :return: tags for all words in sentence
        """
        tagged = []

        for item in self.__replicas:
            tagged.append(pos_tag(word_tokenize(item), lang=self.__language))
        return tagged

    @staticmethod
    def detect_language(sentence):
        return TextBlob(sentence).detect_language()

    @property
    def language(self):
        return self.__language

    # TODO 1) Личное отношение / безличное
    # TODO 2) Официальное / не официальное
    # TODO 3) Доброжелательное или нет
    # TODO 4) Позитивное негативное отношение к собеседнику(!).
    # TODO 5) Уважительное / не уважительное
    # TODO 6) ... !!!



