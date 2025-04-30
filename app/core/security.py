"""
Модуль для работы с паролями и токенами аутентификации.

Функции:
    hash_password: Хеширует пароль с использованием bcrypt.
    verify_password: Проверяет соответствие пароля и его хешированной версии.
    create_access_token: Создаёт JWT токен с истечением срока.
    decode_token: Декодирует JWT токен и извлекает полезную нагрузку.
    get_current_user: Извлекает текущего аутентифицированного пользователя по токену.
"""

from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlmodel import select
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.db.session import get_session
from app.models.models import User
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    """
    Хеширует пароль с использованием bcrypt.

    Параметры:
        password (str): Пароль, который нужно хешировать.

    Возвращает:
        str: Хешированный пароль.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля и его хешированной версии.

    Параметры:
        plain_password (str): Обычный (нехешированный) пароль.
        hashed_password (str): Хешированный пароль.

    Возвращает:
        bool: True, если пароли совпадают, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Создаёт JWT токен с истечением срока.

    Параметры:
        data (dict): Данные, которые нужно включить в токен.
        expires_delta (timedelta, optional): Время жизни токена. 
        По умолчанию используется значение из конфигурации.

    Возвращает:
        str: JWT токен.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    """
    Декодирует JWT токен и извлекает полезную нагрузку.

    Параметры:
        token (str): JWT токен.

    Возвращает:
        str: Имя пользователя, извлечённое из токена, или None, если токен недействителен.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), session = Depends(get_session)) -> User:
    """
    Извлекает текущего аутентифицированного пользователя по токену.

    Параметры:
        token (str): JWT токен.
        session: Сессия базы данных.

    Возвращает:
        User: Объект пользователя.

    Исключения:
        HTTPException: Если токен недействителен или пользователь не найден.
    """
    username = decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Невалидный токен")
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user
