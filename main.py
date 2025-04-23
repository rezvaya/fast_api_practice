from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import uuid

app = FastAPI()

url_store = {}
click_store = {}

class URLRequest(BaseModel):
    user_url: str

@app.post("/short_link")
def short_link(data: URLRequest, request: Request):
    short_id = uuid.uuid4().hex[:6]
    url_store[short_id] = data.user_url
    click_store[short_id] = 0  # Начальный счетчик кликов для нового короткого URL
    short_url = f"{request.base_url}{short_id}"
    return {"short_url": short_url}


@app.get("/{short_id}") 
def redirect(short_id: str):  # Принимаем short_id как параметр
    if short_id not in url_store:
        raise HTTPException(status_code=404, detail="Что-то пошло не так, ссылка не найдена!")
    click_store[short_id] += 1  # Увеличиваем счетчик по short_id
    return RedirectResponse(url=url_store[short_id])


@app.get("/stats/{short_id}")  
def get_stats(short_id: str):  # Принимаем short_id как параметр
    if short_id not in url_store:
        raise HTTPException(status_code=404, detail="Что-то пошло не так, ссылка не найдена!")
    return {"clicks": click_store[short_id]}
