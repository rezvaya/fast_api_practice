"""
Модуль содержит Pydantic-модели для обработки URL-запросов и токенов авторизации.

Классы:
    URLRequest: Модель запроса с URL, введённым пользователем.
    Token: Модель для представления токена доступа и его типа.
"""

from pydantic import BaseModel

class URLRequest(BaseModel):
    """
    Модель запроса, содержащая URL, предоставленный пользователем.
    
    Атрибуты:
        user_url (str): URL, введённый пользователем.
    """
    user_url: str

class Token(BaseModel):
    """
    Модель ответа с токеном авторизации.
    
    Атрибуты:
        access_token (str): Строка токена доступа.
        token_type (str): Тип токена (например, 'bearer').
    """
    access_token: str
    token_type: str
