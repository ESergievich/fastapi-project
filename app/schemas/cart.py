from fastapi.params import Query
from pydantic import BaseModel


class CartItem(BaseModel):
    """Schema for changing an item in the cart"""

    product_id: int = Query(
        ..., description="ID of the product to add/subtract to the cart"
    )
    quantity: int = Query(..., gt=0, description="Quantity must be greater than 0")


class CartResponse(BaseModel):
    """Schema for returning the cart contents"""

    items: dict[str, int]
