from pydantic import BaseModel


class SingleMetric(BaseModel):
    serviceName: str
    path: str
    responseTimeMs: int


class Aggregation(BaseModel):
    path: str
    average: int
    min: int
    max: int
    p99: int
