"""Business aggregation service for the dealership dashboard."""

from app.repositories.purchase_repository import PurchaseRepository
from app.repositories.sale_repository import SaleRepository
from app.repositories.vehicle_repository import VehicleRepository
from app.schemas.dashboard import (
    ActivityType,
    DashboardSummary,
    FinancialMetrics,
    OperationalMetrics,
    RecentActivity,
    RecentActivityResponse,
)


class DashboardService:
    """Compose dashboard metrics from the existing business repositories."""

    _RECENT_ACTIVITY_LIMIT = 10

    def __init__(
        self,
        vehicle_repository: VehicleRepository,
        purchase_repository: PurchaseRepository,
        sale_repository: SaleRepository,
    ) -> None:
        self._vehicle_repository = vehicle_repository
        self._purchase_repository = purchase_repository
        self._sale_repository = sale_repository

    def get_operational_metrics(self) -> OperationalMetrics:
        """Build the current operational snapshot."""
        total_vehicles, available_vehicles, sold_vehicles = (
            self._vehicle_repository.get_operational_counts()
        )
        return OperationalMetrics(
            total_vehicles=total_vehicles,
            available_vehicles=available_vehicles,
            sold_vehicles=sold_vehicles,
            total_purchases=self._purchase_repository.get_count(),
            total_completed_sales=self._sale_repository.get_count(),
        )

    def get_financial_metrics(self) -> FinancialMetrics:
        """Build the current financial snapshot."""
        return FinancialMetrics(
            total_purchase_cost=self._purchase_repository.get_total_purchase_cost(),
            total_sales_revenue=self._sale_repository.get_total_sales_revenue(),
            estimated_gross_profit=self._sale_repository.get_estimated_gross_profit(),
        )

    def get_recent_activity(self) -> RecentActivityResponse:
        """Build a consistently ordered, fixed-size dealership activity feed."""
        purchase_records = self._purchase_repository.get_recent_activity_records(
            self._RECENT_ACTIVITY_LIMIT
        )
        sale_records = self._sale_repository.get_recent_activity_records(
            self._RECENT_ACTIVITY_LIMIT
        )
        activities = [
            RecentActivity(
                activity_type=ActivityType.PURCHASE,
                record_id=record_id,
                vehicle_id=vehicle_id,
                counterparty_name=supplier_name,
                recorded_at=recorded_at,
            )
            for record_id, vehicle_id, supplier_name, recorded_at in purchase_records
        ]
        activities.extend(
            RecentActivity(
                activity_type=ActivityType.SALE,
                record_id=record_id,
                vehicle_id=vehicle_id,
                counterparty_name=customer_name,
                recorded_at=recorded_at,
            )
            for record_id, vehicle_id, customer_name, recorded_at in sale_records
        )
        activities.sort(
            key=lambda activity: (
                activity.recorded_at,
                activity.record_id,
                activity.activity_type.value,
            ),
            reverse=True,
        )
        return RecentActivityResponse(activities=activities[: self._RECENT_ACTIVITY_LIMIT])

    def get_summary(self) -> DashboardSummary:
        """Build the complete dashboard response."""
        return DashboardSummary(
            operational_metrics=self.get_operational_metrics(),
            financial_metrics=self.get_financial_metrics(),
            recent_activity=self.get_recent_activity().activities,
        )
