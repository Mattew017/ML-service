from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from app.main.api.schemas.dataset import CreateDatasetResponse, CreateDatasetRequest
from app.main.api.routers.user import get_current_user_id
from app.application.models.dataset import Dataset, DatasetType
from app.application.protocols.database import UoW, DatasetDatabaseGateway
from app.application.usecases.dataset.create_dataset import create_dataset
from app.application.usecases.dataset.get_by_id import get_dataset_by_id
from app.application.usecases.dataset.get_all import get_all_user_datasets_by_id

import dataclass_factory

dataset_router = APIRouter(prefix='/dataset', tags=['dataset'],
                           route_class=DishkaRoute,
                           dependencies=[Depends(get_current_user_id)])


@dataset_router.post('/create', response_model=CreateDatasetResponse)
async def create(create_request: CreateDatasetRequest,
                 uow: FromDishka[UoW],
                 dataset_gateway: FromDishka[DatasetDatabaseGateway],
                 user_id: int = Depends(get_current_user_id),
                 ):
    factory = dataclass_factory.Factory()
    create_request_dict = create_request.dict()
    create_request_dict['user_id'] = user_id
    dataset: Dataset = factory.load(create_request_dict, Dataset)
    dateset_id = await create_dataset(dataset, uow, dataset_gateway)
    return {'id': dateset_id}


@dataset_router.get('/')
async def get_by_id(dataset_id: int, dataset_gateway: FromDishka[DatasetDatabaseGateway]) -> Dataset:
    dataset = await get_dataset_by_id(dataset_id, dataset_gateway)
    if dataset is None:
        raise HTTPException(status_code=404, detail='Dataset not found')
    return dataset


@dataset_router.get('/all')
async def get_all(dataset_gateway: FromDishka[DatasetDatabaseGateway],
                  dataset_type: DatasetType = DatasetType.TRAIN,
                  user_id: int = Depends(get_current_user_id)) -> list[Dataset]:
    res = await get_all_user_datasets_by_id(user_id, dataset_gateway, dataset_type)
    return res


@dataset_router.delete('/{dataset_id}')
async def delete_by_id(dataset_id: int,
                       uow: FromDishka[UoW],
                       dataset_gateway: FromDishka[DatasetDatabaseGateway]):
    await dataset_gateway.delete_dataset(dataset_id)
    await uow.commit()
