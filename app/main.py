from fastapi import FastAPI
from app.db.database import init_db
from app.routes import url, auth

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(url.router)
app.include_router(auth.router)
