from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from db.session import get_session
from models.models import User
from core.security import hash_password, verify_password, create_access_token
from schemas.schemas import Token
from sqlmodel import select

router = APIRouter()

@router.post("/register")
def register(username: str, password: str, session = Depends(get_session)):
    user_exists = session.exec(select(User).where(User.username == username)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    user = User(username=username, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    return {"message": "Пользователь зарегистрирован"}

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
