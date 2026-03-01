from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.chat import router as chat_router
from .routes.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="SassyAI V2 Chat API")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(chat_router)
    app.include_router(health_router)
    return app


app = create_app()
