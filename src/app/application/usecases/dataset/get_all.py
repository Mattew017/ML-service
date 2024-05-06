from app.application.protocols.database import DatasetDatabaseGateway, UoW


async def get_all_user_datasets_by_id(user_id: int,
                                      dataset_gateway: DatasetDatabaseGateway):
    datasets = await dataset_gateway.get_all_user_datasets(user_id)

    return datasets
