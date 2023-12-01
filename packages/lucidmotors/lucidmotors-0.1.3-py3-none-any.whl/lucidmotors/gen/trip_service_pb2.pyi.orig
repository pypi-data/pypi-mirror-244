from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Waypoint(_message.Message):
    __slots__ = ["latitude", "longitude", "name"]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    name: str
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., name: _Optional[str] = ...) -> None: ...

class Trip(_message.Message):
    __slots__ = ["name", "route"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROUTE_FIELD_NUMBER: _ClassVar[int]
    name: str
    route: _containers.RepeatedCompositeFieldContainer[Waypoint]
    def __init__(self, name: _Optional[str] = ..., route: _Optional[_Iterable[_Union[Waypoint, _Mapping]]] = ...) -> None: ...

class ShareTripRequest(_message.Message):
    __slots__ = ["trip", "vehicle_id"]
    TRIP_FIELD_NUMBER: _ClassVar[int]
    VEHICLE_ID_FIELD_NUMBER: _ClassVar[int]
    trip: Trip
    vehicle_id: str
    def __init__(self, trip: _Optional[_Union[Trip, _Mapping]] = ..., vehicle_id: _Optional[str] = ...) -> None: ...

class ShareTripResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
