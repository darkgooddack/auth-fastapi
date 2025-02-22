from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.models.base import Base, engine
from app.routers import auth, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# Запуск: `uvicorn main:app --reload`
