from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.models import UserTable
from app.application.models.model import Model
from app.application.models.user import User, UserRoleEnum
from app.application.protocols.database import UserDatabaseGateway


class SQLUserDatabaseGateway(UserDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user: User) -> int:
        user_obj = UserTable(username=user.username, password=user.password, role_id=1)
        self.session.add(user_obj)
        await self.session.flush()
        return user_obj.id

    async def get_user_by_id(self, id_: int) -> User:
        res = await self.session.execute(select(UserTable).where(UserTable.id == id_))
        res = res.scalars().first()
        return User(id=res.id, username=res.username, password=res.password, role=UserRoleEnum.USER)

    async def get_by_username(self, username: str) -> User | None:
        res = await self.session.execute(select(UserTable).where(UserTable.username == username))
        res = res.scalars().first()
        if res is None:
            return None
        return User(id=res.id, username=res.username, password=res.password, role=UserRoleEnum.USER)

    async def get_all_users(self) -> list[User]:
        res = await self.session.execute(select(UserTable))
        res = res.scalars().all()
        return [User(id=i.id, username=i.username, password=i.password, role=UserRoleEnum.USER) for i in res]
