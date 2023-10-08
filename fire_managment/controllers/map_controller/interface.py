from pydantic import BaseModel, StrictStr
from typing import Any, Optional

class SelectPointsPayload(BaseModel):
    latitude: int
    longitude: int


class CreatePointPayload(BaseModel):
    longitude : int
    latitude : int
    id: int


class SensorInputPayload(BaseModel):
    id: int
    smoke_level: int
    temperature: int


class MonitoringPayload(BaseModel):
    latitude: int
    longitude: int
    distancia: int
