from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.di.metrics_container import MetricsContainer
from app.domain.entities.metrics import SingleMetric
from app.domain.services.interface.metrics_service_interface import IMetricsService

metrics_router = APIRouter(prefix='/metrics')


@metrics_router.post(
    '',
    status_code=201
)
@inject
async def post_metrics(
        metric: SingleMetric,
        service: IMetricsService = Depends(Provide[MetricsContainer.metrics_service])
):
    await service.register_metric(metric)


@metrics_router.get(
    '/{service_name}'
)
@inject
async def get_metrics(
        service_name: str,
        service: IMetricsService = Depends(Provide[MetricsContainer.metrics_service])
):
    return await service.aggregate_metrics(service_name)
