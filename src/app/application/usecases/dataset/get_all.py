from app.application.models.dataset import DatasetType
from app.application.protocols.database import DatasetDatabaseGateway, UoW


async def get_all_user_datasets_by_id(user_id: int,
                                      dataset_gateway: DatasetDatabaseGateway,
                                      dataset_type: DatasetType):
    datasets = await dataset_gateway.get_all_user_datasets(user_id, dataset_type)

    return datasets
