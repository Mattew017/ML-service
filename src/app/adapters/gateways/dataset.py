from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.adapters.models.datasets import DatasetTable, DatasetDataTable
from app.application.models.dataset import Dataset, DatasetType, DatasetData
from app.application.protocols.database import DatasetDatabaseGateway


class SQLDatasetDatabaseGateway(DatasetDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_dataset(self, dataset: Dataset) -> int:
        type_id = 1 if dataset.type == DatasetType.TRAIN else 2
        dataset_obj = DatasetTable(user_id=dataset.user_id, type_id=type_id, name=dataset.name)
        self.session.add(dataset_obj)
        await self.session.flush()
        dataset_data = [
            DatasetDataTable(dataset_id=dataset_obj.id, param1=i.param1, param2=i.param2, target=i.target)
            for i in dataset.data
        ]

        self.session.add_all(dataset_data)
        return dataset_obj.id

    async def get_dataset_by_id(self, id_: int) -> Dataset:
        result = await self.session.get(DatasetTable, id_)
        dataset_data = await self.session.execute(select(DatasetDataTable).where(DatasetDataTable.dataset_id == id_))
        dataset_type = DatasetType.TRAIN if result.type_id == 1 else DatasetType.TEST
        return Dataset(id=result.id,
                       user_id=result.user_id,
                       name=result.name,
                       type=dataset_type,
                       data=[DatasetData(param1=i.param1, param2=i.param2, target=i.target)
                             for i in dataset_data.scalars().all()])

    async def get_all_user_datasets(self, user_id: int) -> list[Dataset]:
        stmt = select(DatasetTable).where(DatasetTable.user_id == user_id)
        res = await self.session.execute(stmt)
        all_datasets = res.scalars().all()
        result = []
        for dataset in all_datasets:
            dataset_data = await self.session.execute(
                select(DatasetDataTable).where(DatasetDataTable.dataset_id == dataset.id))
            dataset_type = DatasetType.TRAIN if dataset.type_id == 1 else DatasetType.TEST
            result.append(Dataset(id=dataset.id,
                                  user_id=dataset.user_id,
                                  name=dataset.name,
                                  type=dataset_type,
                                  data=[DatasetData(param1=i.param1, param2=i.param2, target=i.target)
                                        for i in dataset_data.scalars().all()]))

        return result
