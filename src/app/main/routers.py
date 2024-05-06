from fastapi import FastAPI
from app.api.routers.index import index_router
from app.api.routers.dataset import dataset_router
from app.api.routers.user import user_router


def init_routers(app: FastAPI):
    app.include_router(index_router)
    app.include_router(dataset_router)
    app.include_router(user_router)
