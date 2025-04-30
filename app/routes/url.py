"""
Этот модуль реализует маршруты FastAPI для сокращения ссылок, редиректа и получения статистики.

Маршруты:
    POST /short_link: Создание сокращённой ссылки для зарегистрированного пользователя.
    GET /{short_id}: Перенаправление по сокращённой ссылке.
    GET /stats/{short_id}: Получение количества переходов по ссылке.
"""

from fastapi import Request, HTTPException, APIRouter, Depends
from fastapi.responses import RedirectResponse
from app.db.session import get_session
from app.models.models import URL
from app.schemas.schemas import URLRequest
from app.core.security import get_current_user

router = APIRouter()

@router.post("/short_link")
def short_link(
    data: URLRequest,
    request: Request,
    user=Depends(get_current_user),
    session=Depends(get_session)):
    """
    Создаёт сокращённую ссылку для переданного URL.

    Параметры:
        data (URLRequest): Объект, содержащий оригинальный URL.
        request (Request): Запрос FastAPI, используется для формирования базового URL.
        user: Аутентифицированный пользователь.
        session: Сессия БД.

    Возвращает:
        dict: Словарь с ключом 'short_url', содержащим сокращённую ссылку.
    """
    url = URL(original_url=data.user_url, owner=user.username)
    session.add(url)
    session.commit()
    session.refresh(url)
    short_url = f"{request.base_url}{url.id}"
    return {"short_url": short_url}


@router.get("/{short_id}")
def redirect(short_id: str, session=Depends(get_session)):
    """
    Перенаправляет пользователя на оригинальный URL по переданному short_id.

    Параметры:
        short_id (str): Идентификатор сокращённой ссылки.
        session: Сессия БД.

    Возвращает:
        RedirectResponse: Редирект на оригинальный URL.
    """
    url = session.get(URL, short_id)
    if not url:
        raise HTTPException(status_code=404, detail="Что-то пошло не так, ссылка не найдена!")
    url.clicks += 1  # Увеличиваем счетчик по short_id
    session.add(url)
    session.commit()
    return RedirectResponse(url=url.original_url)


@router.get("/stats/{short_id}")
def get_stats(short_id: str, session=Depends(get_session)):
    """
    Возвращает статистику (количество переходов) по сокращённой ссылке.

    Параметры:
        short_id (str): Идентификатор сокращённой ссылки.
        session: Сессия БД.

    Возвращает:
        dict: Словарь с количеством переходов ('clicks').
    """
    url = session.get(URL, short_id)
    if not url:
        raise HTTPException(status_code=404, detail="Что-то пошло не так, ссылка не найдена!")
    return {"clicks": url.clicks}
