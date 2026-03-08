from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.data import load_banks
from app.routes import init_banks, router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    banks = load_banks()
    init_banks(banks)
    yield


app = FastAPI(title="Payment Stuff", lifespan=lifespan)
app.include_router(router)
