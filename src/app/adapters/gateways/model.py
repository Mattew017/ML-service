from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.models import ModelTable, ModelEvaluationTable
from app.application.models.model import Model, model_type_to_db
from app.application.protocols.database import ModelDatabaseGateway


class SQLModelDatabaseGateway(ModelDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_train_model(self, model: Model) -> int:
        type_id = model_type_to_db.get(model.type)
        model_obj = ModelTable(dataset_id=model.dataset_id, type_id=type_id)
        self.session.add(model_obj)
        await self.session.flush()
        return model_obj.id

    async def add_eval_model(self, model_id: int, dataset_id: int) -> int:
        eval_model_obj = ModelEvaluationTable(id=model_id, dataset_id=dataset_id)
        self.session.add(eval_model_obj)
        await self.session.flush()
        return eval_model_obj.id

    async def get_train_model(self, model_id: int) -> Model:
        raise NotImplementedError

    async def get_eval_model(self, model_id: int) -> Model:
        raise NotImplementedError
