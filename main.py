from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import logging
import redis

from app.models.base import Base, engine
from app.routers import auth, users

from app.core.config import settings

# try:
#     redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
#     redis_client.ping()
#     logging.info("✅ Подключено к Redis")
# except redis.exceptions.ConnectionError:
#     logging.error("🚨 Ошибка подключения к Redis!")

app = FastAPI(title="Auth API")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# Запуск: `uvicorn main:app --reload`
