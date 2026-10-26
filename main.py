from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.constants import APP_TITLE
from app.data import load_banks


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    load_banks()
    yield


app = FastAPI(title=APP_TITLE, lifespan=lifespan)
app.include_router(router)
