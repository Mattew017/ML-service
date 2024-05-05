from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ModelType(Base):
    __tablename__ = 'model_types'
    name: Mapped[str]


class Model(Base):
    __tablename__ = 'models'
    type_id: Mapped[int] = mapped_column(ForeignKey('model_types.id'))
    dataset_id: Mapped[int] = mapped_column(ForeignKey('datasets.id'))
    progress: Mapped[int] = mapped_column(default=0, server_default="0")


class ModelEvaluation(Base):
    __tablename__ = 'model_evaluations'
    model_id: Mapped[int] = mapped_column(ForeignKey('models.id'))
    dataset_id: Mapped[int] = mapped_column(ForeignKey('datasets.id'))
    progress: Mapped[int] = mapped_column(default=0, server_default="0")
