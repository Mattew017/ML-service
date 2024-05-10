from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserRoleTable(Base):
    __tablename__ = 'user_roles'
    name: Mapped[str]

    users: Mapped[list['UserTable']] = relationship('UserTable', back_populates='role')


class UserTable(Base):
    __tablename__ = 'users'
    username: Mapped[str]
    password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey('user_roles.id'))

    role: Mapped[UserRoleTable] = relationship(UserRoleTable, back_populates='users')
