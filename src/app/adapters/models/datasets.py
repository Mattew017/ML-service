from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models import ModelTable, ModelEvaluationTable
from .base import Base


class DatasetTypeTable(Base):
    __tablename__ = 'dataset_types'
    name: Mapped[str]

    datasets: Mapped[list['DatasetTable']] = relationship('DatasetTable', back_populates='type',
                                                          cascade='all, delete',)


class DatasetTable(Base):
    __tablename__ = 'datasets'
    name: Mapped[str]
    type_id: Mapped[int] = mapped_column(ForeignKey('dataset_types.id', ondelete='CASCADE', onupdate='CASCADE'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'))

    type: Mapped[DatasetTypeTable] = relationship('DatasetTypeTable',
                                                  back_populates='datasets',
                                                  lazy='joined',
                                                  cascade='delete')
    data: Mapped[list['DatasetDataTable']] = relationship('DatasetDataTable', back_populates='dataset')
    train_models: Mapped[list['ModelTable']] = relationship('ModelTable',
                                                            back_populates='dataset',
                                                            lazy='selectin',
                                                            cascade='delete')
    evaluation_models: Mapped[list['ModelEvaluationTable']] = relationship('ModelEvaluationTable',
                                                                           back_populates='evaluation_dataset',
                                                                           lazy='selectin',
                                                                           cascade='delete')


class DatasetDataTable(Base):
    __tablename__ = 'dataset_data'
    dataset_id: Mapped[int] = mapped_column(ForeignKey('datasets.id', ondelete='CASCADE', onupdate='CASCADE'))
    param1: Mapped[float]
    param2: Mapped[float]
    target: Mapped[float]

    dataset: Mapped[DatasetTable] = relationship('DatasetTable',
                                                 back_populates='data',
                                                 cascade='all, delete')
