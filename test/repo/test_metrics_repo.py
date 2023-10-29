import pytest

from app.data.db.database import Database
from app.data.repo.impl.metrics_repo import MetricsRepository
from app.domain.entities.metrics import SingleMetric


@pytest.mark.anyio
async def test_metrics_repo(test_database: Database):
    metrics_repo = MetricsRepository(test_database)
    for i in range(99):
        await metrics_repo.add(
            SingleMetric(
                serviceName='service',
                path='/path',
                responseTimeMs=100,
            )
        )
    await metrics_repo.add(
       SingleMetric(
           serviceName='service',
           path='/path',
           responseTimeMs=200,
       )
    )
    result = await metrics_repo.get_aggregations('service')
    assert result[0].max == 200
    assert result[0].min == 100
    assert result[0].average == 101
    assert result[0].p99 == 100
    await metrics_repo.add(
       SingleMetric(
           serviceName='service',
           path='/path',
           responseTimeMs=200,
       )
    )
    result = await metrics_repo.get_aggregations('service')
    assert result[0].p99 == 200
