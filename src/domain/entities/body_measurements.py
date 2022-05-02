from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from domain.entities.measurement import Measurement


class BodyMeasurements(BaseModel):
    id: Optional[str] = Field(None)
    client_id: int = Field(...)
    measurement_date: datetime = Field(...)
    measurements: List[Measurement] = Field(...)

    def to_map(self) -> dict:
        return {
            "client_id": self.client_id,
            "measurement_date": self.measurement_date,
            "measurements": [x.to_map() for x in self.measurements]
        }
    
    @classmethod
    def from_map(self, doc: dict) -> BaseModel:
        return BodyMeasurements(
            id=str(doc["_id"]),
            client_id=doc["client_id"],
            measurement_date=doc["measurement_date"],
            measurements=[Measurement.from_map(x) for x in doc["measurements"]]
        )

        