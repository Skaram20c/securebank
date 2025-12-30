import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.web.routes import router as web_router
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="SecureBank")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "dev-secret-change-this")
)

app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

app.include_router(web_router)

