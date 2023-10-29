from unittest import mock

import httpx
import pytest
from fastapi import FastAPI
from pydantic import TypeAdapter

from app.domain.entities.metrics import SingleMetric, Aggregation


@pytest.mark.anyio
async def test_post_metric(client: httpx.AsyncClient, _app: FastAPI):
    metric = SingleMetric(
        serviceName='service',
        path='/path',
        responseTimeMs=100,
    )
    service_mock = mock.AsyncMock()
    service_mock.register_metric.return_value = None

    with _app.metrics_container.metrics_service.override(service_mock):
        response = await client.post('/metrics', json=metric.model_dump())
        assert response.status_code == 201


@pytest.mark.anyio
async def test_get_metrics(client: httpx.AsyncClient, _app: FastAPI):
    service_mock = mock.AsyncMock()
    aggregations = [
        Aggregation(
            path='/path',
            average=10,
            min=10,
            max=10,
            p99=10,
        )
    ]
    service_mock.aggregate_metrics.return_value = aggregations
    with _app.metrics_container.metrics_service.override(service_mock):
        response = await client.get('/metrics/service')
        assert response.status_code == 200
        assert TypeAdapter(list[Aggregation]).validate_python(response.json()) == aggregations
