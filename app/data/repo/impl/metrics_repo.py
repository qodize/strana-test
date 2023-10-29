from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.data.db.database import Database
from app.data.db.models.metric_model import MetricModel
from app.domain.entities.metrics import Aggregation, SingleMetric
from app.domain.repo.interface.metrics_repo_interface import IMetricsRepository


class MetricsRepository(IMetricsRepository):
    def __init__(
            self,
            db: Database
    ):
        self._db = db

    async def add(self, metric: SingleMetric):
        async with self._db.get_session() as session:  # type: AsyncSession
            metric = MetricModel(
                serviceName=metric.serviceName,
                path=metric.path,
                responseTimeMs=metric.responseTimeMs
            )
            session.add(metric)
            await session.commit()

    async def get_aggregations(self, service_name: str) -> list[Aggregation]:
        async with self._db.get_session() as session:  # type: AsyncSession
            statement = (
                select(
                    MetricModel.path,
                    func.avg(MetricModel.responseTimeMs),
                    func.min(MetricModel.responseTimeMs),
                    func.max(MetricModel.responseTimeMs),
                    func.percentile_disc(0.99).within_group(MetricModel.responseTimeMs)
                )
                .where(MetricModel.serviceName == service_name)
                .group_by(MetricModel.path)
            )
            result = []
            for a in (await session.execute(statement)).fetchall():
                result.append(
                    Aggregation(
                        path=a[0],
                        average=int(a[1]),
                        min=a[2],
                        max=a[3],
                        p99=a[4]
                    )
                )
            return result
