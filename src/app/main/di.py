from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from app.infrastructure.ioc import create_container


def init_dependencies(app: FastAPI):
    container = create_container()
    setup_dishka(container, app)

