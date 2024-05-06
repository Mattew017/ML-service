from app.application.models.dataset import Dataset
from app.application.protocols.database import DatasetDatabaseGateway, UoW


async def create_dataset(dataset: Dataset,
                         uow: UoW,
                         dataset_gateway: DatasetDatabaseGateway) -> int:
    dataset_id = await dataset_gateway.add_dataset(dataset)
    await uow.commit()
    return dataset_id
