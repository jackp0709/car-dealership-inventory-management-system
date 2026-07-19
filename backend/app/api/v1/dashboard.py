"""Authenticated dashboard aggregation endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.dependencies import get_db
from app.models.user import User
from app.repositories.purchase_repository import PurchaseRepository
from app.repositories.sale_repository import SaleRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.dashboard import (
    DashboardSummary,
    FinancialMetrics,
    OperationalMetrics,
    RecentActivityResponse,
)
from app.services.dashboard_service import DashboardService


router = APIRouter()


def _dashboard_service(session: Session) -> DashboardService:
    """Build a dashboard service using the request-scoped database session."""
    return DashboardService(
        vehicle_repository=VehicleRepository(session),
        purchase_repository=PurchaseRepository(session),
        sale_repository=SaleRepository(session),
    )


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> DashboardSummary:
    """Return a consolidated snapshot of dealership operations."""
    return _dashboard_service(session).get_summary()


@router.get("/operational-metrics", response_model=OperationalMetrics)
def get_operational_metrics(
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> OperationalMetrics:
    """Return current inventory and transaction counts."""
    return _dashboard_service(session).get_operational_metrics()


@router.get("/financial-metrics", response_model=FinancialMetrics)
def get_financial_metrics(
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> FinancialMetrics:
    """Return current aggregate acquisition, revenue, and gross-profit values."""
    return _dashboard_service(session).get_financial_metrics()


@router.get("/recent-activity", response_model=RecentActivityResponse)
def get_recent_activity(
    _: User = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> RecentActivityResponse:
    """Return the ten most recently recorded purchases and sales."""
    return _dashboard_service(session).get_recent_activity()
