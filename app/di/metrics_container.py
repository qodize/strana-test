import os
from os import environ

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from app.data.db.database import Database
from app.data.repo.impl.metrics_repo import MetricsRepository
from app.domain.repo.interface.metrics_repo_interface import IMetricsRepository
from app.domain.services.impl.metrics_service import MetricsService
from app.domain.services.interface.metrics_service_interface import IMetricsService


class MetricsContainer(DeclarativeContainer):
    db: Database = Singleton(
        Database,
        f'postgresql+asyncpg://{environ.get("POSTGRES_USER")}:{environ.get("POSTGRES_PASSWORD")}@{environ.get("POSTGRES_HOST")}:{environ.get("POSTGRES_PORT")}/{environ.get("POSTGRES_DB")}',
        environ.get('DEBUG', 'True') == 'True'
    )

    metrics_repo: IMetricsRepository = Factory(
        MetricsRepository,
        db
    )

    metrics_service: IMetricsService = Factory(
        MetricsService,
        metrics_repo
    )
