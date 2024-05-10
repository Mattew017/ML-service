from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.models.dataset import DatasetType
from app.application.models.metric import MetricsEnum
from app.application.models.model import ModelTypeEnum
from app.application.models.user import UserRoleEnum

dict_router = APIRouter(prefix='/dict', tags=['dict'], route_class=DishkaRoute)


@dict_router.get('/user_types')
async def get_user_types() -> list[str]:
    return [i for i in UserRoleEnum]


@dict_router.get('/dataset_types')
async def get_dataset_types() -> list[str]:
    return [i for i in DatasetType]


@dict_router.get('/model_types')
async def get_model_types() -> list[str]:
    return [i for i in ModelTypeEnum]


@dict_router.get('/metrics')
async def get_metrics() -> list[str]:
    return [i for i in MetricsEnum]


