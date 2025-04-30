from fastapi import Request, HTTPException, APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlmodel import select
from app.db.session import get_session
from app.models.models import URL
from app.schemas.schemas import URLRequest
from app.core.security import get_current_user

router = APIRouter()

@router.post("/short_link")
def short_link(data: URLRequest, request: Request, user=Depends(get_current_user), session=Depends(get_session)):
    url = URL(original_url=data.user_url, owner=user.username)
    session.add(url)
    session.commit()
    session.refresh(url)
    short_url = f"{request.base_url}{url.id}"
    return {"short_url": short_url}


@router.get("/{short_id}") 
def redirect(short_id: str, session=Depends(get_session)):
    url = session.get(URL, short_id)
    if not url:
        raise HTTPException(status_code=404, detail="Что-то пошло не так, ссылка не найдена!")
    url.clicks += 1  # Увеличиваем счетчик по short_id
    session.add(url)
    session.commit()
    return RedirectResponse(url=url.original_url)


@router.get("/stats/{short_id}")  
def get_stats(short_id: str, session=Depends(get_session)):  # Принимаем short_id как параметр
    url = session.get(URL, short_id)
    if not url:
        raise HTTPException(status_code=404, detail="Что-то пошло не так, ссылка не найдена!")
    return {"clicks": url.clicks}