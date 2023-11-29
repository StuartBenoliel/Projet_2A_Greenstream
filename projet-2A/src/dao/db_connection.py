import os
import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from utils.singleton import Singleton


class DBConnection(metaclass = Singleton):
    """
    Classe technique pour ouvrir une seule connexion a la database.
    """
    def __init__(self):
        dotenv.load_dotenv(override = True)
        # Open the connection.
        self.__connection = psycopg2.connect(
            host = os.environ["HOST"],
            port = os.environ["PORT"],
            database = os.environ["DATABASE"],
            user = os.environ["DB_USER"],
            password = os.environ["PASSWORD"],
            cursor_factory = RealDictCursor,
        )

    @property
    def connection(self):
        """
        Retourne la connexion ouverte à la base de données.
        """
        return self.__connection
