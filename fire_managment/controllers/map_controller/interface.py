from pydantic import BaseModel, StrictStr
from typing import Any, Optional

class SelectPointsPayload(BaseModel):
    x_1: int
    x_2: int
    y_1: int
    y_2: int


class CreatePointPayload(BaseModel):
    position_x : int
    position_y : int
    id: int

class SensorInputPayload(BaseModel):
    id: int
    smoke_level: int
    temperature: int
