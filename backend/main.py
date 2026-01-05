import datetime
import pandas as pd

import gtfs_kit as gk


def gtfs_time_to_seconds(time_str: str) -> int:
    if time_str == "":
        return -1
    h, m, s = map(int, time_str.split(":"))
    return h * 3600 + m * 60 + s


def main():
    GTFS_ZIP = "data/gtfs.zip"  # download once, cache locally
    # trip_id,start_time,end_time,headway_secs
    frequencies = pd.read_csv(
        "data/gtfs/frequencies.txt",
        dtype={
            "trip_id": str,
            "headway_secs": int,
        },
        converters={
            "start_time": gtfs_time_to_seconds,
            "end_time": gtfs_time_to_seconds,
        },
    )
    # route_id,service_id,trip_id
    trips = pd.read_csv(
        "data/gtfs/trips.txt",
        dtype={
            "route_id": str,
            "service_id": str,
            "trip_id": str,
        },
    )

    # route_id,agency_id,route_short_name,route_long_name,route_type,route_url
    routes = pd.read_csv(
        "data/gtfs/routes.txt",
        dtype={
            "route_id": str,
            "agency_id": str,
            "route_short_name": str,
            "route_long_name": str,
            "route_type": str,
            "route_url": str,
        },
    )

    # trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,timepoint
    stop_times = pd.read_csv(
        "data/gtfs/stop_times.txt",
        dtype={
            "trip_id": str,
            "stop_id": str,
            "stop_sequence": int,
            "pickup_type": int,
            "drop_off_type": int,
            "timepoint": int,
        },
        converters={
            "arrival_time": gtfs_time_to_seconds,
            "departure_time": gtfs_time_to_seconds,
        },
    )

    routes = routes[routes["agency_id"] == "KMB"]

    science_park_phase_3_stop_id = "13183"
    science_park_phase_3_kmb_stop_ids = [
        "6E821768CA09E8C9",
        "27F96537744C6792",
        "A9459D38A4A41F36",
    ]

    # find trips passing science park phase 3
    science_park_phase_3_stop_times = stop_times[
        stop_times["stop_id"] == science_park_phase_3_stop_id
    ]
    science_park_phase_3_trips = trips[
        trips["trip_id"].isin(science_park_phase_3_stop_times["trip_id"].tolist())
    ]
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)
    print(science_park_phase_3_trips)
    science_park_phase_3_routes = science_park_phase_3_trips["route_id"].unique()
    print(science_park_phase_3_routes)
    science_park_phase_3_frequencies = (
        frequencies[
            frequencies["trip_id"].isin(science_park_phase_3_trips["trip_id"].tolist())
        ]
        # .merge(trips[["trip_id", "route_id"]], on="trip_id", how="left")
        # .merge(routes[["route_id", "route_short_name"]], on="route_id", how="left")
    )
    print(science_park_phase_3_frequencies)


if __name__ == "__main__":
    main()
