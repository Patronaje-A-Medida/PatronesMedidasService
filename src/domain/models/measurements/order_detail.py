from pydantic import BaseModel, Field


class OrderDetail(BaseModel):
    client_id: int = Field(...)
    order_detail_id: int = Field(...)
    garment_id: int = Field(...)
    order_id: int = Field(...)
    