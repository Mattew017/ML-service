from sqlalchemy.ext.asyncio import AsyncSession

from app.application.models.model import Model
from app.application.protocols.database import ModelDatabaseGateway


class SQLModelDatabaseGateway(ModelDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_train_model(self, model: Model) -> int:
        raise NotImplementedError

    async def eval_model(self, model_id: int, dataset_id: int) -> int:
        raise NotImplementedError

    async def get_train_model(self, model_id: int) -> Model:
        raise NotImplementedError

    async def get_eval_model(self, model_id: int) -> Model:
        raise NotImplementedError
