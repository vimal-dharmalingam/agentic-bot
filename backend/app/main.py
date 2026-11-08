import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum

from app.api.routes import router
from app.core.config import get_settings
from app.core.exceptions import LLMProviderError, RepositoryError

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    app.include_router(router)

    @app.exception_handler(LLMProviderError)
    def handle_llm_error(request: Request, exc: LLMProviderError) -> JSONResponse:
        logger.exception("LLM failure")
        return JSONResponse(status_code=502, content={"detail": "AI service unavailable"})

    @app.exception_handler(RepositoryError)
    def handle_repo_error(request: Request, exc: RepositoryError) -> JSONResponse:
        logger.exception("Database failure")
        return JSONResponse(status_code=503, content={"detail": "Storage unavailable"})

    return app


app = create_app()          # used by uvicorn locally
handler = Mangum(app)       # used by AWS Lambda