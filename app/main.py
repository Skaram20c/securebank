from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.web.routes import router as web_router

app = FastAPI(title="SecureBank")

app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

app.include_router(web_router)
