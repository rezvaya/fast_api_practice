"""
Модуль для инициализации базы данных с использованием SQLModel и SQLite.

Функции:
    init_db: Инициализирует базу данных, создавая таблицы, если они не существуют.
"""
from sqlmodel import create_engine, SQLModel

engine = create_engine('sqlite:///./urls.db')

def init_db():
    """
    Инициализирует базу данных, создавая все таблицы, если они не существуют.

    Эта функция использует метаданные SQLModel для создания таблиц в базе данных.
    """
    SQLModel.metadata.create_all(engine)
    