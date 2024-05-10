from fastapi import FastAPI
from app.main.api.routers.dataset import dataset_router
from app.main.api.routers.model import model_router
from app.main.api.routers.user import user_router
from app.main.api.routers.dicts import dict_router


def init_routers(app: FastAPI):
    app.include_router(dict_router)
    app.include_router(user_router)
    app.include_router(dataset_router)
    app.include_router(model_router)
