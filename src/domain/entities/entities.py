from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class BodyMeasurements(BaseModel):
    client_id: int = Field(...)
    measurement_date: datetime = Field(...)