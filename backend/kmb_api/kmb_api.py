from typing import Literal

import aiohttp
from kmb_api_models import (
    EtaListResponse,
    RouteListResponse,
    RouteResponse,
    RouteStopListResponse,
    StopListResponse,
    StopResponse,
)


class KmbApi:
    BASE_URL = "https://data.etabus.gov.hk/"

    async def get_route_list_(self) -> RouteListResponse:
        """This API return all bus routes of KMB."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/v1/transport/kmb/route/"
            ) as response:
                data = await response.json()
                return RouteListResponse.model_validate(data)

    async def get_route(
        self,
        route: str,
        direction: Literal["outbound", "inbound"],
        service_type: int,
    ) -> RouteResponse:
        """
        This API takes a KMB's operating bus route number, direction and service
        type, and returns the respective route information.

        Args:
            route: The route number of the respective bus company. Case sensitive.
            direction: The direction of the route number. Case sensitive. Valid directions are: outbound, inbound.
            service_type: The service type of the bus route.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/v1/transport/kmb/route/{route}/{direction}/{service_type}"
            ) as response:
                data = await response.json()
                return RouteResponse.model_validate(data)

    async def get_stop_list(
        self,
    ) -> StopListResponse:
        """This API returns all bus stop information at once."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/v1/transport/kmb/stop"
            ) as response:
                data = await response.json()
                return StopListResponse.model_validate(data)

    async def get_stop(self, stop_id: str) -> StopResponse:
        """
        This API takes a 16-character bus stop ID and returns the respective bus
        stop information.

        (Remark: To find the corresponding bus stop ID, the user can query the
        "Route-Stop API")

        Args:
            stop_id: 16-character representation of a bus stop. Case sensitive.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/v1/transport/kmb/stop/{stop_id}"
            ) as response:
                data = await response.json()
                return StopResponse.model_validate(data)

    async def get_route_stop_list(self) -> RouteStopListResponse:
        """This API takes returns the stop information of all routes."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/v1/transport/kmb/route-stop"
            ) as response:
                data = await response.json()
                return RouteStopListResponse.model_validate(data)

    async def get_route_stop(
        self, route: str, direction: Literal["outbound", "inbound"], service_type: int
    ) -> RouteStopListResponse:
        """
        This API takes a route direction and the KMB's operating bus route
        number and returns the stop information of the respective route.

        Args:
            route: The route number of the respective bus company. Case sensitive.
            direction: The direction of the route number. Case sensitive. Valid directions are: outbound, inbound.
            service_type: The service type of the bus route.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/v1/transport/kmb/route-stop/{route}/{direction}/{service_type}"
            ) as response:
                data = await response.json()
                return RouteStopListResponse.model_validate(data)

    async def get_eta(
        self, stop_id: str, route: str, service_type: int
    ) -> EtaListResponse:
        """
        This API takes a bus stop ID, the KMB's operating bus route number and
        service type; then, it returns the "estimated time of arrival" (ETA)
        information of the respective route at the stop. Please note that the
        returned ETA information is also included in other service types of the
        same route number if they share the same bus stop.

        (Remark: up to 3 ETA data may be returned for each direction.)

        Args:
            stop_id: 16-character representation of a bus stop. Case sensitive.
            route: The route number of the respective bus company. Case sensitive.
            service_type: The Service type of the bus route. Please note that returned ETA data is also included in other service types of the same route number if they share the same bus stop.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/v1/transport/kmb/eta/{stop_id}/{route}/{service_type}"
            ) as response:
                data = await response.json()
                return EtaListResponse.model_validate(data)

    async def get_stop_eta(self, stop_id: str) -> EtaListResponse:
        """
        This API takes a bus stop ID; then, it returns the "estimated time of
        arrival" (ETA) information of all routes at that stop.

        Please note that the returned ETA information of a route with a service
        type is also included in other service types of the same route number if
        they share the same bus stop.

        Args:
            stop_id: 16-character representation of a bus stop. Case sensitive.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/v1/transport/kmb/stop-eta/{stop_id}"
            ) as response:
                data = await response.json()
                return EtaListResponse.model_validate(data)

    async def get_route_eta(self, route: str, service_type: int) -> EtaListResponse:
        """
        This API takes the KMB's operating bus route number(s) and service
        type(s); then, it returns the "estimated time of arrival" (ETA)
        information of all stops on the respective route. The data format is the
        same as ETA API. Please note that the returned ETA information is also
        included in other service types of the same route number if they share
        the same bus stop.

        Args:
            route: The route number of the respective bus company. Case sensitive.
            service_type: The Service type of the bus route. Please note that returned ETA data is also included in other service types of the same route number if they share the same bus stop.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/v1/transport/kmb/route-eta/{route}/{service_type}"
            ) as response:
                data = await response.json()
                return EtaListResponse.model_validate(data)
