from typing import Generic, Type, Optional, Sequence

from sqlalchemy import select, or_, desc, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from core import ModelType


class BaseCRUD(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, object_in_data: dict, session: AsyncSession) -> ModelType:
        object_db = self.model(**object_in_data)
        session.add(object_db)
        await session.commit()
        await session.refresh(object_db)
        return object_db

    async def get_by_id(
        self, object_id: int, session: AsyncSession
    ) -> Optional[ModelType]:
        return await session.get(self.model, object_id)

    async def get_filtered(
        self,
        session: AsyncSession,
        filters: dict[str, list[str]] | None = None,
        order_by: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[ModelType]:
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

        query = query.limit(limit).offset(offset)
        result = await session.execute(query)
        return result.scalars().all()

    async def update(
        self, object_id: int, update_data: dict, session: AsyncSession
    ) -> ModelType | None:
        stmt = (
            update(self.model)
            .where(self.model.id == object_id)
            .values(**update_data)
            .returning(self.model)
        )

        result = await session.execute(stmt)
        await session.commit()

        return result.scalars().first()

    @staticmethod
    async def delete(object_db: ModelType, session: AsyncSession) -> None:
        await session.delete(object_db)
        await session.commit()
