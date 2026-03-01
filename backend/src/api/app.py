from fastapi import FastAPI

from .routes.chat import router as chat_router
from .routes.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="SassyAI V2 Chat API")
    app.include_router(chat_router)
    app.include_router(health_router)
    return app


app = create_app()
