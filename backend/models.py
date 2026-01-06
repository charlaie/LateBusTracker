from pydantic import BaseModel


class BasicInfo(BaseModel):
    Racecourse: str
    DestEName: str
    OriCName: str
    ServiceTypeENG: str
    DestCName: str
    BusType: str | None
    Airport: str
    ServiceTypeTC: str
    Overnight: str
    ServiceTypeSC: str
    OriSCName: str
    DestSCName: str
    Special: str
    OriEName: str


class RouteStop(BaseModel):
    CName: str
    Y: str
    ELocation: str
    X: str
    AirFare: str
    EName: str
    SCName: str
    ServiceType: str
    CLocation: str
    BSICode: str
    Seq: str
    SCLocation: str
    Direction: str
    Bound: str
    Route: str


class AdditionalInfo(BaseModel):
    ENG: str
    TC: str
    SC: str


class Route(BaseModel):
    lineGeometry: str
    bound: int
    serviceType: int
    route: str


class GetStopsData(BaseModel):
    basicInfo: BasicInfo
    routeStops: list[RouteStop]
    additionalInfo: AdditionalInfo
    route: Route


class GetStopsResponse(BaseModel):
    data: GetStopsData
    result: bool


class GetBoundsData(BaseModel):
    SERVICE_TYPE: int
    BOUND: int
    ROUTE: str


class GetBoundsResponse(BaseModel):
    data: GetBoundsData
    result: bool


class Schedule(BaseModel):
    DayType: str
    BoundTime1: str
    ServiceType_Eng: str
    BoundText1: str
    Origin_Eng: str
    ServiceType: str
    Destination_Chi: str
    OrderSeq: str
    Route: str
    Destination_Eng: str
    BoundTime2: str
    Origin_Chi: str
    BoundText2: str
    ServiceType_Chi: str


class GetScheduleResponse(BaseModel):
    data: dict[str, list[Schedule]]
    result: bool
