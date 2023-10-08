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


class DefineUser(BaseModel):
    user_id: int
    x_1: int
    X_2: int
    y_1: int
    y_2: int
