from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from domain.entities.measurement import Measurement



class BodyMeasurements(BaseModel):
    client_id: int = Field(...)
    measurement_date: datetime = Field(...)
    measurements: List[Measurement] = Field(...)

    def to_map(self) -> dict:
        return {
            "client_id": self.client_id,
            "measurement_date": self.measurement_date,
            "measurements": [x.to_map() for x in self.measurements]
        }
        