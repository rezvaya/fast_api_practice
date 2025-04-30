"""
Модуль содержит ORM-модели SQLModel для таблиц URL и User.

Классы:
    URL: Модель сокращённой ссылки с подсчётом кликов.
    User: Модель пользователя с зашифрованным паролем.
"""

import uuid
from typing import Optional
from sqlmodel import SQLModel, Field

class URL(SQLModel, table=True):
    """
    Модель таблицы URL.

    Атрибуты:
        id (str): Уникальный идентификатор ссылки (6 символов).
        original_url (str): Оригинальная ссылка.
        clicks (int): Количество переходов по ссылке.
        owner (str): Имя пользователя, создавшего ссылку.
    """
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:6], primary_key=True)
    original_url: str
    clicks: int = 0
    owner: str

class User(SQLModel, table=True):
    """
    Модель таблицы пользователей.

    Атрибуты:
        id (int, optional): Уникальный идентификатор пользователя.
        username (str): Имя пользователя (уникальное).
        hashed_password (str): Хешированный пароль.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
