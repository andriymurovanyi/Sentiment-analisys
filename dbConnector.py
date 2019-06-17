# Created by hiddencoder at 05.05.
import mysql.connector


class Connector:
    """
    Connection to DataBase
    """
    def __init__(self):
        self.__cnx = mysql.connector.connect(user="root",
                                             password="123456",
                                             host="localhost",
                                             database="sentimentmodel")
        self.__cursor = self.__cnx.cursor()

    @property
    def cnx(self):
        return self.__cnx

    @property
    def cursor(self):
        return self.__cursor
