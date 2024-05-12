from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.models.datasets import DatasetTable, DatasetDataTable, DatasetTypeTable
from app.application.models.dataset import Dataset, DatasetData, DatasetType
from app.application.protocols.database import DatasetDatabaseGateway


class SQLDatasetDatabaseGateway(DatasetDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_dataset(self, dataset: Dataset) -> int:
        type_id = await self.session.scalar(select(DatasetTypeTable.id).where(DatasetTypeTable.name == dataset.type))
        dataset_obj = DatasetTable(user_id=dataset.user_id, type_id=type_id, name=dataset.name)
        self.session.add(dataset_obj)
        await self.session.flush()
        dataset_data = [
            DatasetDataTable(dataset_id=dataset_obj.id, param1=i.param1, param2=i.param2, target=i.target)
            for i in dataset.data
        ]

        self.session.add_all(dataset_data)
        return dataset_obj.id

    async def get_dataset_by_id(self, id_: int) -> Dataset | None:
        result = await self.session.get(DatasetTable, id_)
        dataset_data = await self.session.execute(select(DatasetDataTable).where(DatasetDataTable.dataset_id == id_))
        if not result:
            return None
        return Dataset(id=result.id,
                       user_id=result.user_id,
                       name=result.name,
                       type=result.type.name,
                       data=[DatasetData(param1=i.param1, param2=i.param2, target=i.target)
                             for i in dataset_data.scalars().all()])

    async def get_all_user_datasets(self, user_id: int, dataset_type: DatasetType) -> list[Dataset]:
        type_id = await self.session.scalar(select(DatasetTypeTable.id).where(DatasetTypeTable.name == dataset_type))
        stmt = (select(DatasetTable).where(DatasetTable.user_id == user_id).
                where(DatasetTable.type_id == type_id))
        res = await self.session.execute(stmt)
        all_datasets = res.scalars().all()
        result = []
        for dataset in all_datasets:
            dataset_data = await self.session.execute(
                select(DatasetDataTable).where(DatasetDataTable.dataset_id == dataset.id))
            result.append(Dataset(id=dataset.id,
                                  user_id=dataset.user_id,
                                  name=dataset.name,
                                  type=dataset.type.name,
                                  data=[DatasetData(param1=i.param1, param2=i.param2, target=i.target)
                                        for i in dataset_data.scalars().all()]))

        return result

    async def delete_dataset(self, dataset_id: int) -> None:
        stmt = delete(DatasetTable).where(DatasetTable.id == dataset_id)
        await self.session.execute(stmt)


