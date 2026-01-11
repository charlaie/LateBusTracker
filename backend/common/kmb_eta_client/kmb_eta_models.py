from pydantic import BaseModel


class RouteData(BaseModel):
    """The object that of the data requested."""

    route: str
    """The bus route number. Route services of KMB and LWB are included."""
    bound: str
    """The direction of the bus route. The direction can be: I - inbound, O - outbound."""
    service_type: str
    """The service type of the bus route."""
    orig_en: str
    """The origin of a bus route in English."""
    orig_tc: str
    """The origin of a bus route in Traditional Chinese."""
    orig_sc: str
    """The origin of a bus route in Simplified Chinese."""
    dest_en: str
    """The destination of a bus route in English."""
    dest_tc: str
    """The destination of a bus route in Traditional Chinese."""
    dest_sc: str
    """The destination of a bus route in Simplified Chinese."""


class RouteResponse(BaseModel):
    """Route response model."""

    type: str
    """The corresponding API that returns the data. The value will always be "Route" or "RouteList"."""
    version: str
    """The version number of the JSON returned. The version number in major and minor versioning format."""
    generated_timestamp: str
    """The timestamp of the initial generated time of the response before it is cached. Date time with the time zone in ISO 8601 format."""
    data: RouteData
    """The object that of the data requested. Empty data object denotes data not available. For the List API, data is returned in an array of objects."""


class RouteListResponse(BaseModel):
    """Route List response model."""

    type: str
    """The corresponding API that returns the data. The value will always be "Route" or "RouteList"."""
    version: str
    """The version number of the JSON returned. The version number in major and minor versioning format."""
    generated_timestamp: str
    """The timestamp of the initial generated time of the response before it is cached. Date time with the time zone in ISO 8601 format."""
    data: list[RouteData]
    """The object that of the data requested. Empty data object denotes data not available. For the List API, data is returned in an array of objects."""


class StopData(BaseModel):
    """The object that of the data requested."""

    stop: str
    """The ID of a bus stop."""
    name_tc: str
    """The name of a bus stop, in Traditional Chinese"""
    name_en: str
    """The name of a bus stop, in English."""
    name_sc: str
    """The name of a bus stop, in Simplified Chinese."""
    lat: str
    """Latitude of a bus stop location. Latitude in decimal degree in WGS84 standard."""
    long: str
    """Longitude of a bus stop location. Longitude in decimal degree in WGS84 standard."""


class StopResponse(BaseModel):
    """Stop response model."""

    type: str
    """The corresponding API that returns the data. The value will always be "Stop" or "StopList"."""
    version: str
    """The version number of the JSON returned. The version number in major and minor versioning format."""
    generated_timestamp: str
    """The timestamp of the initial generated time of the response before it is cached. Date time with the time zone in ISO 8601 format."""
    data: StopData
    """The object that of the data requested. Empty data object denotes data not available. For the List API, data is returned in an array of objects."""


class StopListResponse(BaseModel):
    """Stop List response model."""

    type: str
    """The corresponding API that returns the data. The value will always be "Stop" or "StopList"."""
    version: str
    """The version number of the JSON returned. The version number in major and minor versioning format."""
    generated_timestamp: str
    """The timestamp of the initial generated time of the response before it is cached. Date time with the time zone in ISO 8601 format."""
    data: list[StopData]
    """The object that of the data requested. Empty data object denotes data not available. For the List API, data is returned in an array of objects."""


class RouteStopData(BaseModel):
    """The object that of the data requested."""

    route: str
    """The bus route number of the requested bus company."""
    bound: str
    """The direction of the bus route. The value can be: I - inbound, O - outbound."""
    service_type: str
    """The service type of the bus route."""
    seq: int
    """The stop sequence number of a bus route."""
    stop: str
    """The ID of a bus stop."""


class RouteStopListResponse(BaseModel):
    """Route-Stop List response model."""

    type: str
    """The corresponding API that returns the data. The value will always be "RouteStop" or "RouteStopList"."""
    version: str
    """The version number of the JSON returned. The version number in major and minor versioning format."""
    generated_timestamp: str
    """The timestamp of the initial generated time of the response before it is cached. Date time with the time zone in ISO 8601 format."""
    data: list[RouteStopData]
    """The object that of the data requested. Empty data object denotes data not available. For the List API, data is returned in an array of objects."""


class EtaData(BaseModel):
    """The object that of the data requested."""

    route: str
    """The bus route number of the requested bus company."""
    dir: str
    """The direction of the bus route. The direction can be: I - inbound, O - outbound."""
    service_type: int
    """The service type of the bus route."""
    seq: int
    """The stop sequence number of a bus route."""
    # stop: str | None = None
    """The ID of a bus stop."""
    dest_tc: str
    """The destination of a bus route in Traditional Chinese."""
    dest_sc: str
    """The destination of a bus route in Simplified Chinese."""
    dest_en: str
    """The destination of a bus route in English."""
    eta_seq: int
    """The sequence number of ETA."""
    eta: str | None
    """The timestamp of the next ETA. Date time with the time zone in ISO 8601 format."""
    rmk_tc: str
    """The remark of an ETA in Traditional Chinese."""
    rmk_sc: str
    """The remark of an ETA in Simplified Chinese."""
    rmk_en: str
    """The remark of an ETA in English."""


class EtaListResponse(BaseModel):
    """Stop ETA / Route ETA response model."""

    type: str
    """The corresponding API that returns the data. The value will always be "ETA", "StopETA" or "RouteETA"."""
    version: str
    """The version number of the JSON returned. The version number in major and minor versioning format."""
    generated_timestamp: str
    """The timestamp of the initial generated time of the response before it is cached. Date time with the time zone in ISO 8601 format."""
    data: list[EtaData]
    """The object that of the data requested. Empty data object denotes data not available."""


class EtaDictResponse(BaseModel):
    """ETA dictionary response model."""

    type: str
    """The corresponding API that returns the data. The value will always be "ETA", "StopETA" or "RouteETA"."""
    version: str
    """The version number of the JSON returned. The version number in major and minor versioning format."""
    generated_timestamp: str
    """The timestamp of the initial generated time of the response before it is cached. Date time with the time zone in ISO 8601 format."""
    data: dict[int, EtaData]
    """The object that of the data requested. Empty data object denotes data not available."""
