from typing import Optional, List
from pydantic import BaseModel, Field

from domain.entities.pattern_dimension import PatternDimension


class PatternGarmentAdjusted(BaseModel):
    id: Optional[str] = Field(None)
    order_detail_id: int = Field(...)
    client_id: int = Field(...)
    garment_id: int = Field(...)
    order_id: int = Field(...)
    image: str = Field(None)
    dimensions: List[PatternDimension] = Field(None)

    def to_map(self) -> dict:
        return {
            "id": self.id,
            "order_deatil_id": self.order_detail_id,
            "client_id": self.client_id,
            "garment_id": self.garment_id,
            "order_id": self.order_id,
            "image": self.image,
            "dimensions": [x.to_map() for x in self.dimensions]
        }
    
    @classmethod
    def from_map(self, doc: dict) -> BaseModel:
        return PatternGarmentAdjusted(
            id=str(doc["_id"]),
            order_detail_id=doc["order_detail_id"],
            client_id=doc["client_id"],
            garment_id=doc["garment_id"],
            order_id=doc["order_id"],
            image=doc["image"],
            dimensions=[PatternDimension.from_map(x) for x in doc["dimensions"]]
        )
