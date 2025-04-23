from fastapi import FastAPI
from db.database import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()




