from datetime import datetime

from pydantic import BaseModel, Field

from schemas import OrderItemCreate, OrderItemResponse, OrderItemUpdate


class OrderCreate(BaseModel):
    user_id: int
    order_items: list[OrderItemCreate]


class OrderUpdate(BaseModel):
    user_id: int | None = None
    order_items: list[OrderItemUpdate] | None = None


class OrderResponse(OrderCreate):
    id: int
    created_at: datetime
    order_items: list[OrderItemResponse]


class OrderFilterIn(BaseModel):
    id: list[int] = Field(default_factory=list)
    user_id: list[int] = Field(default_factory=list)

    class Config:
        extra = "forbid"
