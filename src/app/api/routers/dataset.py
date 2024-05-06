from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import Depends
from fastapi.routing import APIRouter

from app.api.routers.schemas.dataset import CreateDatasetResponse, CreateDatasetRequest
from app.api.routers.user import get_current_user_id
from app.application.models.dataset import Dataset
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
    create_request_dict['id'] = 0
    dataset: Dataset = factory.load(create_request_dict, Dataset)
    dateset_id = await create_dataset(dataset, uow, dataset_gateway)
    return {'id': dateset_id}


@dataset_router.get('/')
async def get_by_id(dataset_id: int, dataset_gateway: FromDishka[DatasetDatabaseGateway]) -> Dataset:
    dataset = await get_dataset_by_id(dataset_id, dataset_gateway)
    return dataset


@dataset_router.get('/all')
async def get_all(dataset_gateway: FromDishka[DatasetDatabaseGateway],
                  user_id: int = Depends(get_current_user_id)) -> list[Dataset]:
    res = await get_all_user_datasets_by_id(user_id, dataset_gateway)
    return res
