from typing import Type, Generic

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core import ModelType, UpdateSchemaType, CreateSchemaType


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, crud, model: Type[ModelType]):
        self.crud = crud
        self.model = model

    async def create(
        self, object_in: CreateSchemaType, session: AsyncSession
    ) -> ModelType:
        return await self.crud.create(object_in, session)

    async def get_by_id(self, object_id: int, session: AsyncSession) -> ModelType:
        object_db = await self.crud.get(object_id, session)
        if not object_db:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} with ID {object_id} not found",
            )
        return object_db

    async def get_filtered(
        self, filter_query, session: AsyncSession
    ) -> list[ModelType]:
        filters = filter_query.get_parsed_tags()
        return await self.crud.get_filtered(
            session=session,
            filters=filters,
            order_by=filter_query.order_by,
            limit=filter_query.limit,
            offset=filter_query.offset,
        )

    async def update(
        self, object_id: int, object_in: UpdateSchemaType, session: AsyncSession
    ) -> ModelType:
        object_db = await self.get_by_id(object_id, session)
        return await self.crud.update(object_db, object_in, session)

    async def delete(self, object_id: int, session: AsyncSession) -> None:
        object_db = await self.get_by_id(object_id, session)
        await self.crud.delete(object_db, session)

    async def find_by_attr(
        self, attr_name: str, value: str, session: AsyncSession
    ) -> list[ModelType]:
        if not hasattr(self.model, attr_name):
            raise HTTPException(
                status_code=400, detail=f"Invalid attribute: {attr_name}"
            )

        attr = getattr(self.model, attr_name)
        return await self.crud.find_by_attr(attr, value, session)

    async def find_by_attrs(
        self, attrs: dict[str, str], session: AsyncSession, operator: str = "and"
    ) -> list[ModelType]:
        for attr_name, value in attrs.items():
            if not hasattr(self.model, attr_name):
                raise HTTPException(
                    status_code=400, detail=f"Invalid attribute: {attr_name}"
                )

        attrs = {getattr(self.model, attr): value for attr, value in attrs.items()}
        return await self.crud.find_by_attrs(attrs, operator, session)
