
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.protocols.database import UoW


class SQLUnitOfWork(UoW):
    __slots__ = ("session",)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
