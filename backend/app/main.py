from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.router import api_router
from app.core.config import get_settings
from app.core.exception_handlers import register_exception_handlers


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )
    register_exception_handlers(application)
    application.include_router(health_router)
    application.include_router(api_router)
    return application


app = create_application()
