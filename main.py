from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.data import load_banks
from app.routes import router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    load_banks()
    yield


app = FastAPI(title="Payment Stuff", lifespan=lifespan)
app.include_router(router)
