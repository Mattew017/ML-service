from dataclasses import dataclass, field
from enum import Enum


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"


@dataclass
class User:
    id: int
    username: str
    password: str
    role: UserRoleEnum
