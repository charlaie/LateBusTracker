import asyncio

import aiohttp

from .kmb_api_models import GetBoundsResponse, GetScheduleResponse, GetStopsResponse


class KmbApiClient:
    async def get_bounds(self, route_id: str) -> GetBoundsResponse:
        url = f"https://search.kmb.hk/KMBWebSite/Function/FunctionRequest.ashx?action=getroutebound&route={route_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                data = GetBoundsResponse.model_validate(data)
                return data

    async def get_schedule(self, route_id: str, bound: int) -> GetScheduleResponse:
        url = f"https://search.kmb.hk/KMBWebSite/Function/FunctionRequest.ashx?action=getschedule&route={route_id}&bound={bound}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                data = GetScheduleResponse.model_validate(data)
                return data

    async def get_stops(self, route_id: str, bound: int) -> GetStopsResponse:
        url = f"https://search.kmb.hk/KMBWebSite/Function/FunctionRequest.ashx?action=getstops&route={route_id}&bound={bound}&serviceType=1"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                data = GetStopsResponse.model_validate(data)
                return data


if __name__ == "__main__":
    result = asyncio.run(KmbApiClient().get_schedule("272s", 1))
    print(result.model_dump_json(indent=2))
