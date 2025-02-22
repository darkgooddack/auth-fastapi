import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.crud.user import get_user_by_username

router = APIRouter()
logging.basicConfig(level=logging.INFO)


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logging.info(f"Запрос авторизации для пользователя: {form_data.username}")

    user = get_user_by_username(db, form_data.username)

    if not user:
        logging.error("Ошибка: пользователь не найден!")
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not verify_password(form_data.password, user.hashed_password):
        logging.error("Ошибка: неверный пароль!")
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    logging.info(f"Выдан токен пользователю: {user.username}")

    return {"access_token": access_token, "token_type": "bearer"}

