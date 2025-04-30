"""
Основной модуль приложения FastAPI.

Инициализирует базу данных при запуске и подключает маршруты 
для аутентификации и управления ссылками.
"""

from fastapi import FastAPI
from app.db.database import init_db
from app.routes import url, auth

app = FastAPI()

@app.on_event("startup")
def on_startup():
    """
    Обработчик события запуска приложения.
    Инициализирует базу данных.
    """
    init_db()

# Подключение маршрутов
app.include_router(url.router)
app.include_router(auth.router)
