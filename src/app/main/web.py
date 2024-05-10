from fastapi import FastAPI

from .di import init_dependencies
from .routers import init_routers

import asyncio
import sys


def create_app() -> FastAPI:
    app = FastAPI()
    init_routers(app)
    init_dependencies(app)
    return app
