from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class DatasetTypeTable(Base):
    __tablename__ = 'dataset_types'
    name: Mapped[str]


class DatasetTable(Base):
    __tablename__ = 'datasets'
    name: Mapped[str]
    type_id: Mapped[int] = mapped_column(ForeignKey('dataset_types.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


class DatasetDataTable(Base):
    __tablename__ = 'dataset_data'
    dataset_id: Mapped[int] = mapped_column(ForeignKey('datasets.id'))
    param1: Mapped[float]
    param2: Mapped[float]
    target: Mapped[float]
