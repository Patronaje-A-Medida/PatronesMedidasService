from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Measurement(BaseModel):
    name_measurement: str = Field(...)
    value: float = Field(...)
    acronym: str = Field(...)
    units: str = Field(...)

    def to_json(self) -> dict:
        return {
            "name_measurement": self.name_measurement,
            "value": self.value,
            "acronym": self.acronym,
            "units": self.units
        }
    
class BodyMeasurements(BaseModel):
    client_id: int = Field(...)
    measurement_date: datetime = Field(...)
    measurements: List[Measurement] = Field(...)

    def to_json(self) -> dict:
        return {
            "client_id": self.client_id,
            "measurement_date": self.measurement_date,
            "measurements": [x.to_json() for x in self.measurements]
        }