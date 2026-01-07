from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_db_session, init_db
from .ingest.kmb import ingest_kmb_reference_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Late Bus Tracker API", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, bool]:
    return {"ok": True}


@app.post("/admin/ingest/kmb")
async def ingest_kmb(session: AsyncSession = Depends(get_db_session)) -> dict[str, int]:
    return await ingest_kmb_reference_data(session)


