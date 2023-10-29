from unittest import mock

import pytest

from app.domain.entities.metrics import SingleMetric, Aggregation
from app.domain.services.impl.metrics_service import MetricsService


@pytest.mark.anyio
async def test_register_metric():
    repo_mock = mock.AsyncMock()
    repo_mock.add.return_value = None
    metrics_service = MetricsService(repo_mock)
    await metrics_service.register_metric(SingleMetric(
        serviceName='service',
        path='/path',
        responseTimeMs=100,
    ))


@pytest.mark.anyio
async def test_aggregate_metrics():
    repo_mock = mock.AsyncMock()
    aggregations = [
        Aggregation(
            path='/path',
            average=100,
            min=100,
            max=100,
            p99=100,
        )
    ]
    repo_mock.get_aggregations.return_value = aggregations
    metrics_service = MetricsService(repo_mock)
    result = await metrics_service.aggregate_metrics('service')
    assert result == aggregations
