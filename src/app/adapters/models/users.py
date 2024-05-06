from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UserRoleTable(Base):
    __tablename__ = 'user_roles'
    name: Mapped[str]


class UserTable(Base):
    __tablename__ = 'users'
    username: Mapped[str]
    password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey('user_roles.id'))
