import typing

from app.domain.entities.metrics import SingleMetric, Aggregation


class IMetricsRepository(typing.Protocol):
    async def add(self, metric: SingleMetric):
        ...

    async def get_aggregations(self, service_name: str) -> list[Aggregation]:
        ...
