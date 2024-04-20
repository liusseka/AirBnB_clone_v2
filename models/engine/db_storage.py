#!/usr/bin/python3
"""new class for abstracting storage using sqlAlchemy"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base 
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """Manages interactions with a storage database """

    __engine = None
    __session = None

    def __init__(self):
        """Initializes the database storage instance."""
        self._config = {
            'user': getenv("HBNB_MYSQL_USER"),
            'passwd': getenv("HBNB_MYSQL_PWD"),
            'db': getenv("HBNB_MYSQL_DB"),
            'host': getenv("HBNB_MYSQL_HOST"),
            'env': getenv("HBNB_ENV")
        }
        self.__engine = self._get_engine()
        if self._config['env'] == "test":
            Base.metadata.drop_all(self.__engine)
            self._config['db'] = 'hbnb_clone_test'  # Use a test database
            self.__engine = self._get_engine()

    def _get_engine(self):
        """Creates the database engine."""
        return create_engine('mysql+mysqldb://{}:{}@{}/{}'
                             .format(self._config['user'],
                                     self._config['passwd'],
                                     self._config['host'],
                                     self._config['db']),
                             pool_pre_ping=True)

    def all(self, cls: type = None) -> dict:
        """Queries the database and returns a dictionary of objects.

        Args:
            cls (type, optional): The class to filter results by. Defaults to None.

        Returns:
            dict: A dictionary where keys are in the format "<class_name>.<id>"
                  and values are the corresponding objects.
        """
        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                dic[key] = elem
        else:
            lista = [State, City, User, Place, Review, Amenity]
            for clase in lista:
                query = self.__session.query(clase)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    dic[key] = elem
        return (dic)

    def new(self, obj: object) -> None:
        """Adds a new object to the session.

        Args:
            obj (object): The object to be added.
        """
        self.__session.add(obj)

    def save(self) -> None:
        """Commits all changes to the database."""
        self.__session.commit()

    def delete(self, obj: object = None) -> None:
        """Deletes an object from the session.

        Args:
            obj (object, optional): The object to be deleted. Defaults to None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self) -> None:
        """Creates database tables and initializes a session factory."""
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self) -> None:
        """Closes the current session."""
        self.__session.close()

