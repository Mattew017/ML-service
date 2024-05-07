from dishka import FromDishka
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import Depends
from fastapi.routing import APIRouter

from app.api.routers.user import get_current_user_id
from app.application.models.model import Model, ModelTypeEnum
from app.application.protocols.database import UoW, ModelDatabaseGateway

model_router = APIRouter(prefix='/model', tags=[' model'],
                         route_class=DishkaRoute,
                         dependencies=[Depends(get_current_user_id)])


@model_router.post('/train_model')
async def create_train_model(dataset_id: int,
                             model_type: ModelTypeEnum,
                             uow: FromDishka[UoW],
                             model_gateway: FromDishka[ModelDatabaseGateway]
                             ) -> int:
    model = Model(dataset_id=dataset_id, type=model_type)
    res = await model_gateway.add_train_model(model)
    return res


@model_router.post('/eval_model')
async def create_eval_model(dataset_id: int,
                            model_id: int,
                            uow: FromDishka[UoW],
                            model_gateway: FromDishka[ModelDatabaseGateway]
                            ) -> int:
    res = await model_gateway.add_eval_model(model_id, dataset_id)
    return res


@model_router.get('train_model')
async def get_train_model(model_id: int,
                          model_gateway: FromDishka[ModelDatabaseGateway]) -> Model:
    model = await model_gateway.get_train_model(model_id)
    return model


@model_router.get('eval_model')
async def get_eval_model(model_id: int,
                         model_gateway: FromDishka[ModelDatabaseGateway]) -> Model:
    model = await model_gateway.get_eval_model(model_id)
    return model
