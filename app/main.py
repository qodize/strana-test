import uvicorn
from fastapi import FastAPI

from app.api.metrics import metrics_router
from app.di.metrics_container import MetricsContainer


def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(metrics_router)
    metrics_container = MetricsContainer()
    metrics_container.wire(packages=['app.api'])
    app.metrics_container = metrics_container
    return app


app = get_app()

if __name__ == '__main__':
    uvicorn.run(app)
