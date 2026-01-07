from __future__ import annotations

from sqlalchemy import Float, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class KmbRoute(Base):
    __tablename__ = "kmb_routes"

    # Composite primary key matches KMB uniqueness.
    route: Mapped[str] = mapped_column(String(10), primary_key=True)
    bound: Mapped[str] = mapped_column(String(1), primary_key=True)  # "I" / "O"
    service_type: Mapped[str] = mapped_column(String(4), primary_key=True)

    orig_en: Mapped[str] = mapped_column(String(200))
    orig_tc: Mapped[str] = mapped_column(String(200))
    orig_sc: Mapped[str] = mapped_column(String(200))

    dest_en: Mapped[str] = mapped_column(String(200))
    dest_tc: Mapped[str] = mapped_column(String(200))
    dest_sc: Mapped[str] = mapped_column(String(200))

    __table_args__ = (Index("ix_kmb_routes_route", "route"),)


class KmbStop(Base):
    __tablename__ = "kmb_stops"

    stop_id: Mapped[str] = mapped_column(String(16), primary_key=True)
    name_tc: Mapped[str] = mapped_column(String(200))
    name_en: Mapped[str] = mapped_column(String(200))
    name_sc: Mapped[str] = mapped_column(String(200))

    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)


class KmbRouteStop(Base):
    __tablename__ = "kmb_route_stops"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    route: Mapped[str] = mapped_column(String(10), nullable=False)
    bound: Mapped[str] = mapped_column(String(1), nullable=False)
    service_type: Mapped[str] = mapped_column(String(4), nullable=False)

    seq: Mapped[int] = mapped_column(Integer, nullable=False)
    stop_id: Mapped[str] = mapped_column(String(16), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "route",
            "bound",
            "service_type",
            "seq",
            name="uq_kmb_route_stops_route_bound_service_seq",
        ),
        Index("ix_kmb_route_stops_stop_id", "stop_id"),
        Index("ix_kmb_route_stops_route", "route"),
    )
