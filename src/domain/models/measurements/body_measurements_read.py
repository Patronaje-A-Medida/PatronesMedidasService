from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

from domain.entities.measurement import Measurement


class BodyMeasurementsRead(BaseModel):
    id: str = Field(...)
    client_id: int = Field(...)
    measurement_date: datetime = Field(...)
    measurements: List[Measurement] = Field(...)

    def to_map(self) -> dict:
        return {
            "id": self.id,
            "client_id": self.client_id,
            "measurement_date": str(self.measurement_date.isoformat()),
            "measurements": [x.to_map() for x in self.measurements]
        }
    