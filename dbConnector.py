import mysql.connector



class Connector:
    """
    Connection to database
    """

    def __init__(self):
        self.__cnx = mysql.connector.connect(user="root", password="Kjkszpj",
                                             host="localhost", database="sentimentmodel")
        self.__cursor = self.__cnx.cursor()

    @property
    def cnx(self):
        return self.__cnx

    @property
    def cursor(self):
        return self.__cursor


connector = Connector()
print(connector.cnx)
print(connector.cursor)
