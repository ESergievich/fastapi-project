from typing import Optional, Sequence

from sqlalchemy import select, or_, desc, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, InstrumentedAttribute, selectinload

from crud import BaseCRUD
from models import Order, OrderItem
from schemas import OrderCreate, OrderResponse, OrderUpdate


class OrderCRUD(BaseCRUD[Order, OrderCreate, OrderResponse]):
    async def create(self, order_in: OrderCreate, session: AsyncSession) -> Order:
        new_order = Order(user_id=order_in.user_id)
        session.add(new_order)
        await session.flush()

        for item in order_in.order_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
            )
            session.add(order_item)

        await session.commit()
        return await self.get_by_id(new_order.id, session)

    async def get_by_id(self, order_id: int, session: AsyncSession) -> Optional[Order]:
        result = await session.execute(
            select(Order)
            .options(joinedload(Order.order_items))
            .where(Order.id == order_id)
        )
        return result.scalars().first()

    async def get_filtered(
        self,
        session: AsyncSession,
        filters: dict[str, list[str]] | None = None,
        order_by: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Order]:
        query = select(self.model)
        if filters:
            conditions = []
            for field_name, values in filters.items():
                column: InstrumentedAttribute | None = getattr(
                    self.model, field_name, None
                )
                conditions.append(column.in_(values))
            query = query.where(or_(*conditions))

        if order_by:
            order_column = getattr(self.model, order_by, None)
            if order_column is not None:
                query = query.order_by(desc(order_column))

        query = (
            query.options(selectinload(Order.order_items)).limit(limit).offset(offset)
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def update(
        self, order_id: int, order_in: OrderUpdate, session: AsyncSession
    ) -> Optional[Order]:
        order = await self.get_by_id(order_id, session)
        if not order:
            return None

        if order_in.user_id:
            order.user_id = order_in.user_id

        if order_in.order_items:
            for item_update in order_in.order_items:
                for order_item in order.order_items:
                    if order_item.product_id == item_update.product_id:
                        if item_update.quantity:
                            order_item.quantity = item_update.quantity
                        break
                else:
                    if item_update.product_id and item_update.quantity:
                        new_order_item = OrderItem(
                            product_id=item_update.product_id,
                            quantity=item_update.quantity,
                            order_id=order.id,
                        )
                        session.add(new_order_item)

            order_item_ids_to_delete = [
                item.product_id
                for item in order.order_items
                if item.product_id
                not in [item_update.product_id for item_update in order_in.order_items]
            ]
            if order_item_ids_to_delete:
                stmt = select(OrderItem).filter(
                    OrderItem.product_id.in_(order_item_ids_to_delete)
                )
                items_to_delete = await session.execute(stmt)
                for item in items_to_delete.scalars():
                    await session.delete(item)

        await session.commit()
        await session.refresh(order)
        return order


order_crud = OrderCRUD(Order)
