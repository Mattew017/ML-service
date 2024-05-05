from fastapi import FastAPI
from app.api.routers.index import index_router


def init_routers(app: FastAPI):
    app.include_router(index_router)
