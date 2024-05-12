from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from datasets import DatasetTable

from .base import Base


class ModelTypeTable(Base):
    __tablename__ = 'model_types'
    name: Mapped[str]

    models: Mapped[list['ModelTable']] = relationship('ModelTable',
                                                      back_populates='model_type',
                                                      cascade='all, delete')


class ModelTable(Base):
    __tablename__ = 'models'
    type_id: Mapped[int] = mapped_column(ForeignKey('model_types.id', ondelete='CASCADE', onupdate='CASCADE'))
    dataset_id: Mapped[int] = mapped_column(ForeignKey('datasets.id', ondelete='CASCADE', onupdate='CASCADE'))
    progress: Mapped[int] = mapped_column(default=0, server_default="0")

    dataset: Mapped['DatasetTable'] = relationship('DatasetTable',
                                                   back_populates='train_models',
                                                   cascade='delete')
    model_type: Mapped['ModelTypeTable'] = relationship(ModelTypeTable,
                                                        back_populates='models',
                                                        lazy='joined',
                                                        cascade='delete')
    evaluations: Mapped[list['ModelEvaluationTable']] = relationship('ModelEvaluationTable',
                                                                     back_populates='train_model',
                                                                     cascade='delete')


class ModelEvaluationTable(Base):
    __tablename__ = 'model_evaluations'
    model_id: Mapped[int] = mapped_column(ForeignKey('models.id', ondelete='CASCADE', onupdate='CASCADE'))
    dataset_id: Mapped[int] = mapped_column(ForeignKey('datasets.id', ondelete='CASCADE', onupdate='CASCADE'))
    progress: Mapped[int] = mapped_column(default=0, server_default="0")

    evaluation_dataset: Mapped['DatasetTable'] = relationship('DatasetTable',
                                                              back_populates='evaluation_models',
                                                              cascade='delete')

    train_model: Mapped['ModelTable'] = relationship(ModelTable,
                                                     back_populates='evaluations',
                                                     lazy='joined',
                                                     cascade='delete')
