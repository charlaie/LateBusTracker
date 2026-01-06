import requests

from models import GetBoundsResponse, GetScheduleResponse, GetStopsResponse


def get_bounds(route_id: str) -> GetBoundsResponse:
    url = f"https://search.kmb.hk/KMBWebSite/Function/FunctionRequest.ashx?action=getroutebound&route={route_id}"
    response = requests.get(url)
    data = response.json()
    data = GetBoundsResponse.model_validate(data)
    return data


def get_schedule(route_id: str, bound: int) -> GetScheduleResponse:
    url = f"https://search.kmb.hk/KMBWebSite/Function/FunctionRequest.ashx?action=getschedule&route={route_id}&bound={bound}"
    response = requests.get(url)
    data = response.json()
    data = GetScheduleResponse.model_validate(data)
    return data


def get_stops(route_id: str, bound: int) -> GetStopsResponse:
    url = f"https://search.kmb.hk/KMBWebSite/Function/FunctionRequest.ashx?action=getstops&route={route_id}&bound={bound}&serviceType=1"
    response = requests.get(url)
    data = response.json()
    data = GetStopsResponse.model_validate(data)
    return data


if __name__ == "__main__":
    print(get_schedule("272s", 1).model_dump_json(indent=2))
