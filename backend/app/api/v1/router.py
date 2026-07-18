"""Version 1 API router registration."""

from fastapi import APIRouter

from app.api.health import router as health_router


router = APIRouter()
router.include_router(health_router)
