from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.models import ModelTable, ModelEvaluationTable
from app.application.models.model import Model, model_type_to_db
from app.application.protocols.database import ModelDatabaseGateway


class SQLModelDatabaseGateway(ModelDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_train_model(self, model: Model) -> int:
        type_id = model_type_to_db.get(model.type)
        model_obj = ModelTable(dataset_id=model.dataset_id, type_id=type_id, progress=100)
        self.session.add(model_obj)
        await self.session.flush()
        return model_obj.id

    async def add_eval_model(self, model_id: int, dataset_id: int) -> int:
        eval_model_obj = ModelEvaluationTable(model_id=model_id, dataset_id=dataset_id, progress=100)
        self.session.add(eval_model_obj)
        await self.session.flush()
        return eval_model_obj.id

    async def get_train_model(self, model_id: int) -> Model | None:
        stmt = (select(ModelTable).where(ModelTable.id == model_id))
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if not res:
            return None

        return Model(id=res.id, dataset_id=res.dataset_id, progress=res.progress, type=res.model_type.name)

    async def get_eval_model(self, model_id: int) -> Model | None:
        stmt = (select(ModelEvaluationTable).where(ModelEvaluationTable.id == model_id))
        res = await self.session.execute(stmt)
        res = res.scalar_one_or_none()
        if not res:
            return None

        return Model(id=res.id, dataset_id=res.dataset_id,
                     progress=res.progress,
                     type=res.train_model.model_type.name)

    async def get_all_train_models(self, dataset_id: int) -> list[Model]:
        all_models = await self.session.execute(select(ModelTable).where(ModelTable.dataset_id == dataset_id))
        all_models = all_models.scalars().all()
        return [Model(id=model.id,
                      dataset_id=model.dataset_id,
                      progress=model.progress,
                      type=model.model_type.name) for model in all_models]

    async def get_all_eval_models(self, dataset_id: int) -> list[Model]:
        all_models = await self.session.execute(select(ModelEvaluationTable)
                                                .where(ModelEvaluationTable.dataset_id == dataset_id))
        all_models = all_models.scalars().all()
        return [Model(id=model.id,
                      dataset_id=model.dataset_id,
                      progress=model.progress,
                      type=model.train_model.model_type.name)
                for model in all_models]

    async def delete_train_model(self, model_id: int) -> None:
        stmt = delete(ModelTable).where(ModelTable.id == model_id)
        await self.session.execute(stmt)

    async def delete_eval_model(self, eval_model_id: int) -> None:
        stmt = delete(ModelEvaluationTable).where(ModelEvaluationTable.id == eval_model_id)
        await self.session.execute(stmt)

