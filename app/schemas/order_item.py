from typing import Optional

from pydantic import BaseModel, Field, field_validator


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)


class OrderItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None

    @field_validator("quantity")
    def validate_quantity(cls, v):
        if v and v <= 0:
            raise ValueError("quantity must be greater than 0")
        return v


class OrderItemResponse(OrderItemCreate):
    pass
