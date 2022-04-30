from pydantic import BaseModel, Field



class Measurement(BaseModel):
    name_measurement: str = Field(...)
    value: float = Field(...)
    acronym: str = Field(...)
    units: str = Field(...)

    def to_map(self) -> dict:
        return {
            "name_measurement": self.name_measurement,
            "value": self.value,
            "acronym": self.acronym,
            "units": self.units
        }
