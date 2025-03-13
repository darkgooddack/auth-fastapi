from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import logging
import redis

from app.models.base import Base, engine
from app.routers import auth, users, job

from app.core.config import settings


app = FastAPI(title="Auth API", root_path="/api/v1")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")
app.include_router(job.router, prefix="/vacancy")

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# Запуск: `uvicorn main:app --reload`
