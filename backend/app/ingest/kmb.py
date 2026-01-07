from __future__ import annotations

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from kmb_api import KmbApi

from ..models import KmbRoute, KmbRouteStop, KmbStop


async def ingest_kmb_reference_data(
    session: AsyncSession, api: KmbApi | None = None
) -> dict[str, int]:
    """Ingest relatively-static KMB reference data into Postgres.

    Currently ingests:
    - Route list
    - Stop list
    - Route-stop list
    """

    api = api or KmbApi()

    route_list = await api.get_route_list_()
    routes_rows = [
        {
            "route": r.route,
            "bound": r.bound,
            "service_type": r.service_type,
            "orig_en": r.orig_en,
            "orig_tc": r.orig_tc,
            "orig_sc": r.orig_sc,
            "dest_en": r.dest_en,
            "dest_tc": r.dest_tc,
            "dest_sc": r.dest_sc,
        }
        for r in route_list.data
    ]
    if routes_rows:
        stmt = insert(KmbRoute).values(routes_rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["route", "bound", "service_type"],
            set_={
                "orig_en": stmt.excluded.orig_en,
                "orig_tc": stmt.excluded.orig_tc,
                "orig_sc": stmt.excluded.orig_sc,
                "dest_en": stmt.excluded.dest_en,
                "dest_tc": stmt.excluded.dest_tc,
                "dest_sc": stmt.excluded.dest_sc,
            },
        )
        await session.execute(stmt)

    stop_list = await api.get_stop_list()
    stops_rows = [
        {
            "stop_id": s.stop,
            "name_tc": s.name_tc,
            "name_en": s.name_en,
            "name_sc": s.name_sc,
            "lat": float(s.lat),
            "lon": float(s.long),
        }
        for s in stop_list.data
    ]
    if stops_rows:
        stmt = insert(KmbStop).values(stops_rows)
        stmt = stmt.on_conflict_do_update(
            index_elements=["stop_id"],
            set_={
                "name_tc": stmt.excluded.name_tc,
                "name_en": stmt.excluded.name_en,
                "name_sc": stmt.excluded.name_sc,
                "lat": stmt.excluded.lat,
                "lon": stmt.excluded.lon,
            },
        )
        await session.execute(stmt)

    route_stop_list = await api.get_route_stop_list()
    route_stops_rows = [
        {
            "route": rs.route,
            "bound": rs.bound,
            "service_type": rs.service_type,
            "seq": rs.seq,
            "stop_id": rs.stop,
        }
        for rs in route_stop_list.data
    ]
    if route_stops_rows:
        stmt = insert(KmbRouteStop).values(route_stops_rows)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_kmb_route_stops_route_bound_service_seq",
            set_={"stop_id": stmt.excluded.stop_id},
        )
        await session.execute(stmt)

    await session.commit()

    return {
        "routes": len(routes_rows),
        "stops": len(stops_rows),
        "route_stops": len(route_stops_rows),
    }


