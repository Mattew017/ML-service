import random

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter

from app.main.api.routers.user import get_current_user_id
from app.main.api.schemas.model import GetModelResponseSchema
from app.application.models.metric import MetricsEnum, Metric
from app.application.models.model import Model, ModelTypeEnum
from app.application.protocols.database import UoW, ModelDatabaseGateway, MetricDatabaseGateway

model_router = APIRouter(prefix='/model', tags=[' model'],
                         route_class=DishkaRoute,
                         dependencies=[Depends(get_current_user_id)])


def create_metrics() -> list[Metric]:
    result = []
    for metric_name in MetricsEnum.ACCURACY, MetricsEnum.PRECISION, MetricsEnum.RECALL, MetricsEnum.F1:
        random_value = random.random()
        result.append(Metric(name=metric_name.value, value=random_value))

    return result


@model_router.post('/train')
async def create_train_model(dataset_id: int,
                             model_type: ModelTypeEnum,
                             uow: FromDishka[UoW],
                             model_gateway: FromDishka[ModelDatabaseGateway],
                             metric_gateway: FromDishka[MetricDatabaseGateway]
                             ) -> int:
    model = Model(dataset_id=dataset_id, type=model_type)
    model_id = await model_gateway.add_train_model(model)
    metrics = create_metrics()
    for metric in metrics:
        await metric_gateway.add_train_metric(model_id, metric)
    await uow.commit()
    return model_id


@model_router.post('/eval')
async def create_eval_model(dataset_id: int,
                            model_id: int,
                            uow: FromDishka[UoW],
                            model_gateway: FromDishka[ModelDatabaseGateway],
                            metric_gateway: FromDishka[MetricDatabaseGateway]
                            ) -> int:
    eval_model_id = await model_gateway.add_eval_model(model_id, dataset_id)
    metrics = create_metrics()
    for metric in metrics:
        await metric_gateway.add_eval_metric(eval_model_id, metric)
    await uow.commit()
    return eval_model_id


@model_router.get('/train/{model_id}', response_model=GetModelResponseSchema)
async def get_train_model(model_id: int,
                          model_gateway: FromDishka[ModelDatabaseGateway],
                          metric_gateway: FromDishka[MetricDatabaseGateway]):
    model = await model_gateway.get_train_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail='Model not found')
    model_metrics = await metric_gateway.get_train_metrics(model_id)
    result = GetModelResponseSchema(model=model, metrics=model_metrics)
    return result


@model_router.get('/eval/{model_id}', response_model=GetModelResponseSchema)
async def get_eval_model(model_id: int,
                         model_gateway: FromDishka[ModelDatabaseGateway],
                         metric_gateway: FromDishka[MetricDatabaseGateway], ):
    model = await model_gateway.get_eval_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail='Model not found')
    model_metrics = await metric_gateway.get_eval_metrics(model_id)
    return GetModelResponseSchema(model=model, metrics=model_metrics)


@model_router.get('/train/all/{dataset_id}', response_model=list[GetModelResponseSchema])
async def get_all_train_models(model_gateway: FromDishka[ModelDatabaseGateway],
                               metric_gateway: FromDishka[MetricDatabaseGateway],
                               dataset_id: int):
    result = []
    models = await model_gateway.get_all_train_models(dataset_id)
    for model in models:
        model_metrics = await metric_gateway.get_train_metrics(model.id)
        result.append(GetModelResponseSchema(model=model, metrics=model_metrics))
    return result


@model_router.get('/eval/all/{dataset_id}', response_model=list[GetModelResponseSchema])
async def get_all_eval_models(model_gateway: FromDishka[ModelDatabaseGateway],
                              metric_gateway: FromDishka[MetricDatabaseGateway],
                              dataset_id: int):
    result = []
    models = await model_gateway.get_all_eval_models(dataset_id)
    for model in models:
        model_metrics = await metric_gateway.get_eval_metrics(model.id)
        result.append(GetModelResponseSchema(model=model, metrics=model_metrics))
    return result
