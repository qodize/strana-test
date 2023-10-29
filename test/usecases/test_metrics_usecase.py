import httpx
import pytest

from app.domain.entities.metrics import SingleMetric, Aggregation


@pytest.mark.anyio
async def test_get_metrics(client: httpx.AsyncClient):
    for i in range(99):
        metric = SingleMetric(
            serviceName='service',
            path='/path',
            responseTimeMs=100,
        )
        await client.post('/metrics', json=metric.model_dump())
    metric = SingleMetric(
        serviceName='service',
        path='/path',
        responseTimeMs=200,
    )
    await client.post('/metrics', json=metric.model_dump())

    response = await client.get('/metrics/service')

    assert response.status_code == 200
    data = Aggregation.model_validate(response.json()[0])
    assert data.max == 200
    assert data.min == 100
    assert data.average == 101
    assert data.p99 == 100

    await client.post('/metrics', json=metric.model_dump())
    response = await client.get('/metrics/service')

    assert response.status_code == 200
    data = Aggregation.model_validate(response.json()[0])
    assert data.p99 == 200
