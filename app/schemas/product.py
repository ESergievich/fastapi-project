from datetime import datetime
from typing import Optional

from pydantic import BaseModel, condecimal, Field


class ProductCreate(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    price: condecimal(gt=0, decimal_places=2)


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    price: Optional[condecimal(gt=0, decimal_places=2)] = None


class ProductResponse(ProductCreate):
    id: int
    created_at: datetime
    updated_at: datetime


class ProductFilterIn(BaseModel):
    id: list[int] = Field(default_factory=list)
    name: list[str] = Field(default_factory=list)
    slug: list[str] = Field(default_factory=list)

    class Config:
        extra = "forbid"
