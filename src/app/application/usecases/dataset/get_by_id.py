from app.application.protocols.database import DatasetDatabaseGateway


async def get_dataset_by_id(dataset_id: int,
                            dataset_gateway: DatasetDatabaseGateway):
    dataset = await dataset_gateway.get_dataset_by_id(dataset_id)

    return dataset
