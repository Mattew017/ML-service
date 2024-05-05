from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Metric(Base):
    __tablename__ = 'metrics'
    name: Mapped[str]


class TrainMetrics(Base):
    __tablename__ = 'train_metrics'
    metric_id: Mapped[int] = mapped_column(ForeignKey('metrics.id'))
    model_id: Mapped[int] = mapped_column(ForeignKey('models.id'))
    value: Mapped[float]


class EvaluationMetrics(Base):
    __tablename__ = 'evaluation_metrics'
    metric_id: Mapped[int] = mapped_column(ForeignKey('metrics.id'))
    model_id: Mapped[int] = mapped_column(ForeignKey('models.id'))
    value: Mapped[float]
