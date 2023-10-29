import typing

from app.domain.entities.metrics import SingleMetric, Aggregation


class IMetricsService(typing.Protocol):
    async def register_metric(self, metric: SingleMetric):
        ...

    async def aggregate_metrics(self, service_name: str) -> list[Aggregation]:
        ...
