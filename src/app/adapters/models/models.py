from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from datasets import DatasetTable

from .base import Base


class ModelTypeTable(Base):
    __tablename__ = 'model_types'
    name: Mapped[str]

    models: Mapped[list['ModelTable']] = relationship('ModelTable', back_populates='model_type')


class ModelTable(Base):
    __tablename__ = 'models'
    type_id: Mapped[int] = mapped_column(ForeignKey('model_types.id'))
    dataset_id: Mapped[int] = mapped_column(ForeignKey('datasets.id'))
    progress: Mapped[int] = mapped_column(default=0, server_default="0")

    dataset: Mapped['DatasetTable'] = relationship('DatasetTable', back_populates='train_models')
    model_type: Mapped['ModelTypeTable'] = relationship(ModelTypeTable, back_populates='models', lazy='joined')
    evaluations: Mapped[list['ModelEvaluationTable']] = relationship('ModelEvaluationTable',
                                                                     back_populates='train_model')


class ModelEvaluationTable(Base):
    __tablename__ = 'model_evaluations'
    model_id: Mapped[int] = mapped_column(ForeignKey('models.id'))
    dataset_id: Mapped[int] = mapped_column(ForeignKey('datasets.id'))
    progress: Mapped[int] = mapped_column(default=0, server_default="0")

    evaluation_dataset: Mapped['DatasetTable'] = relationship('DatasetTable', back_populates='evaluation_models')

    train_model: Mapped['ModelTable'] = relationship(ModelTable, back_populates='evaluations', lazy='joined')
