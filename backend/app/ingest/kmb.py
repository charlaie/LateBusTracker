from __future__ import annotations
import asyncio

from collections.abc import Mapping, Sequence

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import AsyncSessionLocal, get_db_session, init_db
from common.kmb_eta_client import KmbEtaClient
from common.kmb_api_client import KmbApiClient

from app.models import (
    KmbRoute,
    KmbRouteStop,
    KmbStop,
    KmbWebRouteBound,
    KmbWebRouteStop,
    KmbWebSchedule,
)


def _chunks(
    rows: Sequence[Mapping[str, object]], size: int
) -> list[Sequence[Mapping[str, object]]]:
    """Split rows into batches to avoid asyncpg's max bind-parameter limit."""
    return [rows[i : i + size] for i in range(0, len(rows), size)]


async def ingest_kmb_reference_data(
    session: AsyncSession, eta_client: KmbEtaClient | None = None
) -> dict[str, int]:
    """Ingest relatively-static KMB reference data into Postgres.

    Currently ingests:
    - Route list
    - Stop list
    - Route-stop list
    """

    eta_client = eta_client or KmbEtaClient()

    route_list = await eta_client.get_route_list_()
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
        for batch in _chunks(routes_rows, 300):
            stmt = insert(KmbRoute).values(batch)
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

    stop_list = await eta_client.get_stop_list()
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
        for batch in _chunks(stops_rows, 300):
            stmt = insert(KmbStop).values(batch)
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

    route_stop_list = await eta_client.get_route_stop_list()
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
        for batch in _chunks(route_stops_rows, 300):
            stmt = insert(KmbRouteStop).values(batch)
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


async def ingest_kmb_web_stops_and_schedule(
    session: AsyncSession,
    route_id: str,
    api: KmbApiClient | None = None,
) -> dict[str, int]:
    """Ingest route-specific KMB data from the KMB 'search' site API.

    Ingests:
    - Bounds (getroutebound) [fetched once]
    - Stops per bound (getstops) [fetched per bound]
    - Schedule (getschedule) [saved once; fetched for the first bound]
    """

    api = api or KmbApiClient()

    bounds_resp = await api.get_bounds(route_id)
    bounds_rows = [
        {"route": b.ROUTE, "bound": int(b.BOUND), "service_type": int(b.SERVICE_TYPE)}
        for b in bounds_resp.data
    ]
    if bounds_rows:
        for batch in _chunks(bounds_rows, 500):
            stmt = insert(KmbWebRouteBound).values(batch)
            stmt = stmt.on_conflict_do_update(
                index_elements=["route", "bound", "service_type"],
                set_={"service_type": stmt.excluded.service_type},
            )
            await session.execute(stmt)

    # Fetch stops for each bound we discovered.
    stops_rows: list[dict[str, object]] = []
    unique_bounds = (
        sorted({int(b["bound"]) for b in bounds_rows}) if bounds_rows else []
    )
    for bound in unique_bounds:
        stops_resp = await api.get_stops(route_id, bound)
        for rs in stops_resp.data.routeStops:
            stops_rows.append(
                {
                    "route": rs.Route,
                    "bound": int(rs.Bound),
                    "service_type": int(rs.ServiceType),
                    "seq": int(rs.Seq),
                    "bsi_code": rs.BSICode,
                    "c_name": rs.CName,
                    "e_name": rs.EName,
                    "sc_name": rs.SCName,
                    "c_location": rs.CLocation,
                    "e_location": rs.ELocation,
                    "sc_location": rs.SCLocation,
                    "x": float(rs.X),
                    "y": float(rs.Y),
                    "air_fare": rs.AirFare,
                    "direction": rs.Direction,
                }
            )

    if stops_rows:
        for batch in _chunks(stops_rows, 200):
            stmt = insert(KmbWebRouteStop).values(batch)
            stmt = stmt.on_conflict_do_update(
                index_elements=["route", "bound", "service_type", "seq"],
                set_={
                    "bsi_code": stmt.excluded.bsi_code,
                    "c_name": stmt.excluded.c_name,
                    "e_name": stmt.excluded.e_name,
                    "sc_name": stmt.excluded.sc_name,
                    "c_location": stmt.excluded.c_location,
                    "e_location": stmt.excluded.e_location,
                    "sc_location": stmt.excluded.sc_location,
                    "x": stmt.excluded.x,
                    "y": stmt.excluded.y,
                    "air_fare": stmt.excluded.air_fare,
                    "direction": stmt.excluded.direction,
                },
            )
            await session.execute(stmt)

    # Schedule: per your requirement, store it once (it appears identical across bounds).
    schedule_rows: list[dict[str, object]] = []
    if unique_bounds:
        schedule_resp = await api.get_schedule(route_id, unique_bounds[0])
        for service_type_key, rows in schedule_resp.data.items():
            for r in rows:
                # Some fields in the payload contain padding spaces; keep them trimmed.
                service_type = (r.ServiceType or service_type_key).strip()
                schedule_rows.append(
                    {
                        "route": r.Route.strip(),
                        "service_type": service_type,
                        "day_type": r.DayType.strip(),
                        "order_seq": int(r.OrderSeq.strip()),
                        "bound_time_1": r.BoundTime1.strip(),
                        "bound_text_1": r.BoundText1.strip(),
                        "bound_time_2": r.BoundTime2.strip(),
                        "bound_text_2": r.BoundText2.strip(),
                        "origin_eng": r.Origin_Eng.strip(),
                        "origin_chi": r.Origin_Chi.strip(),
                        "destination_eng": r.Destination_Eng.strip(),
                        "destination_chi": r.Destination_Chi.strip(),
                        "service_type_eng": r.ServiceType_Eng.strip(),
                        "service_type_chi": r.ServiceType_Chi.strip(),
                    }
                )

    if schedule_rows:
        for batch in _chunks(schedule_rows, 150):
            stmt = insert(KmbWebSchedule).values(batch)
            stmt = stmt.on_conflict_do_update(
                index_elements=["route", "service_type", "day_type", "order_seq"],
                set_={
                    "bound_time_1": stmt.excluded.bound_time_1,
                    "bound_text_1": stmt.excluded.bound_text_1,
                    "bound_time_2": stmt.excluded.bound_time_2,
                    "bound_text_2": stmt.excluded.bound_text_2,
                    "origin_eng": stmt.excluded.origin_eng,
                    "origin_chi": stmt.excluded.origin_chi,
                    "destination_eng": stmt.excluded.destination_eng,
                    "destination_chi": stmt.excluded.destination_chi,
                    "service_type_eng": stmt.excluded.service_type_eng,
                    "service_type_chi": stmt.excluded.service_type_chi,
                },
            )
            await session.execute(stmt)

    await session.commit()

    return {
        "bounds": len(bounds_rows),
        "web_route_stops": len(stops_rows),
        "web_schedules": len(schedule_rows),
    }


async def main():
    await init_db()
    async with get_db_session() as session:
        result = await session.execute(select(KmbRoute))
        routes = result.scalars().all()
        print(f"Found {len(routes)} routes")
        for route in routes:
            print(
                f"Route: {route.route}, Bound: {route.bound}, Service Type: {route.service_type}"
            )

        result = await ingest_kmb_reference_data(session)
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
