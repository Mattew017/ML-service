from sqlalchemy.ext.asyncio import AsyncSession

from app.application.models.model import Model
from app.application.models.user import User
from app.application.protocols.database import UserDatabaseGateway


class SQLModelDatabaseGateway(UserDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user: User) -> None:
        raise NotImplementedError

    async def get_user_by_id(self, id_: int) -> User:
        raise NotImplementedError
