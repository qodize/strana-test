from sqlalchemy.orm import Mapped, mapped_column

from app.data.db.models import Base


class MetricModel(Base):
    __tablename__ = 'metrics'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    serviceName: Mapped[str]
    path: Mapped[str]
    responseTimeMs: Mapped[int]
