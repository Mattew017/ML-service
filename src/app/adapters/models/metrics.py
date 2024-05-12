from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class MetricTable(Base):
    __tablename__ = 'metrics'
    name: Mapped[str]

    train_metrics: Mapped[list['TrainMetricsTable']] = relationship(
        'TrainMetricsTable', back_populates='metric', cascade='all, delete'
    )
    evaluation_metrics: Mapped[list['EvaluationMetricsTable']] = relationship(
        'EvaluationMetricsTable', back_populates='metric', cascade='all, delete'
    )


class TrainMetricsTable(Base):
    __tablename__ = 'train_metrics'
    metric_id: Mapped[int] = mapped_column(ForeignKey('metrics.id', ondelete='CASCADE', onupdate='CASCADE'))
    model_id: Mapped[int] = mapped_column(ForeignKey('models.id', ondelete='CASCADE', onupdate='CASCADE'))
    value: Mapped[float]

    metric: Mapped[MetricTable] = relationship(
        'MetricTable',
        back_populates='train_metrics',
        lazy='joined',
        cascade='delete'
    )


class EvaluationMetricsTable(Base):
    __tablename__ = 'evaluation_metrics'
    metric_id: Mapped[int] = mapped_column(ForeignKey('metrics.id', ondelete='CASCADE', onupdate='CASCADE'))
    model_id: Mapped[int] = mapped_column(ForeignKey('model_evaluations.id', ondelete='CASCADE', onupdate='CASCADE'))
    value: Mapped[float]

    metric: Mapped[MetricTable] = relationship(
        'MetricTable',
        back_populates='evaluation_metrics',
        lazy='joined',
        cascade='delete'
    )
