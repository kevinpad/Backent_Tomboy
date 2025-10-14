from fastapi import FastAPI
from .core.config import settings
from .core.cors import add_cors
from .api.routes.chat_routes import router as chat_router              
from .api.routes.chat_openai_routes import router as chat_openai_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)
    add_cors(app)
    app.include_router(chat_router)
    app.include_router(chat_openai_router)
    return app

app = create_app()