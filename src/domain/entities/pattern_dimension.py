from pydantic import BaseModel, Field


class PatternDimension(BaseModel):
    label: str = Field(...)
    value: float = Field(...)
    units: str = Field(...)

    def to_map(self) -> dict:
        return {
            "label": self.label,
            "value": self.value,
            "units": self.units
        }
    
    @classmethod
    def from_map(self, doc: dict) -> BaseModel:
        return PatternDimension(
            label=doc["label"],
            value=doc["value"],
            units=doc["units"]
        )