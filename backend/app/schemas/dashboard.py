"""Pydantic schemas for dealership dashboard responses."""

from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class ActivityType(str, Enum):
    """Business events displayed in the dashboard activity feed."""

    PURCHASE = "PURCHASE"
    SALE = "SALE"


class OperationalMetrics(BaseModel):
    """Aggregated dealership inventory and transaction counts."""

    total_vehicles: int
    available_vehicles: int
    sold_vehicles: int
    total_purchases: int
    total_completed_sales: int


class FinancialMetrics(BaseModel):
    """Aggregated financial values derived from recorded transactions."""

    total_purchase_cost: Decimal
    total_sales_revenue: Decimal
    estimated_gross_profit: Decimal


class RecentActivity(BaseModel):
    """A recent purchase or sale recorded by the dealership."""

    activity_type: ActivityType
    record_id: int
    vehicle_id: int
    counterparty_name: str
    recorded_at: datetime


class RecentActivityResponse(BaseModel):
    """Limited recent activity feed for dashboard presentation."""

    activities: list[RecentActivity]


class DashboardSummary(BaseModel):
    """Consolidated dashboard data for a single frontend request."""

    operational_metrics: OperationalMetrics
    financial_metrics: FinancialMetrics
    recent_activity: list[RecentActivity]
