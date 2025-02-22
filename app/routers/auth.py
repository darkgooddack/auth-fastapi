import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.crud.user import get_user_by_username
from app.schemas.user import UserCreate

router = APIRouter()
logging.basicConfig(level=logging.INFO)


@router.post(
    "/token",
    summary="Авторизация пользователя",
    description="""
    Аутентифицирует пользователя и выдаёт JWT-токен.  
    Используйте полученный токен для доступа к защищённым ресурсам.
    """,
    responses={
        200: {"description": "Успешная аутентификация, возвращается токен"},
        400: {"description": "Неверное имя пользователя или пароль"}
    },
)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    """
    **Авторизация пользователя**
    - 🔑 Проверяет логин и пароль.
    - 🎫 Возвращает JWT-токен для доступа к защищённым API.
    - ❌ Ошибка, если логин или пароль неверные.
    """

    logging.info(f"✅ Запрос авторизации для пользователя: {user.username}")

    db_user = get_user_by_username(db, user.username)

    if not db_user:
        logging.error("❌ Ошибка: пользователь не найден!")
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if not verify_password(user.password, db_user.hashed_password):
        logging.error("❌ Ошибка: неверный пароль!")
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": db_user.username})
    logging.info(f"✅ Выдан токен пользователю: {db_user.username}")

    return {"access_token": access_token, "token_type": "bearer"}

