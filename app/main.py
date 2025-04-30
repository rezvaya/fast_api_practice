from fastapi import FastAPI
from db.database import init_db
from routes import url, auth 

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(url.router)
app.include_router(auth.router)