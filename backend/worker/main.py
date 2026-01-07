from __future__ import annotations

import asyncio

from app.db import AsyncSessionLocal, init_db
from app.ingest.kmb import ingest_kmb_reference_data
from app.settings import get_settings


async def run_once() -> dict[str, int]:
    async with AsyncSessionLocal() as session:
        return await ingest_kmb_reference_data(session)


async def main() -> None:
    settings = get_settings()
    await init_db()

    # Basic poll loop; adjust later to ingest ETA snapshots, compute "lateness", etc.
    while True:
        result = await run_once()
        print(f"[worker] ingested kmb reference data: {result}")
        await asyncio.sleep(settings.poll_interval_seconds)


if __name__ == "__main__":
    asyncio.run(main())


