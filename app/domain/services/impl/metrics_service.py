from app.domain.entities.metrics import SingleMetric, Aggregation
from app.domain.repo.interface.metrics_repo_interface import IMetricsRepository
from app.domain.services.interface.metrics_service_interface import IMetricsService


class MetricsService(IMetricsService):
    def __init__(
            self,
            metrics_repo: IMetricsRepository
    ):
        self._metrics_repo = metrics_repo

    async def register_metric(self, metric: SingleMetric):
        await self._metrics_repo.add(metric)

    async def aggregate_metrics(self, service_name: str) -> list[Aggregation]:
        return await self._metrics_repo.get_aggregations(service_name)
