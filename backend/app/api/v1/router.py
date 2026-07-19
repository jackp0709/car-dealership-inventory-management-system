"""Version 1 API router registration."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.purchases import router as purchases_router
from app.api.v1.sales import router as sales_router
from app.api.v1.users import router as users_router
from app.api.v1.vehicles import router as vehicles_router
from app.api.health import router as health_router


router = APIRouter()
router.include_router(health_router)
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(vehicles_router, prefix="/vehicles", tags=["Vehicles"])
router.include_router(purchases_router, prefix="/purchases", tags=["Purchases"])
router.include_router(sales_router, prefix="/sales", tags=["Sales"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
