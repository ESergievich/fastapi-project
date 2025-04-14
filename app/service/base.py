from typing import Type, Generic, TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from errors import ObjectNotFound, ForbiddenAccess
from type_vars import ModelType, CreateSchemaType, UpdateSchemaType
from utils import RoleEnum

if TYPE_CHECKING:
    from models import User


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, crud, model: Type[ModelType]):
        self.crud = crud
        self.model = model

    async def create(
        self, object_in: CreateSchemaType, session: AsyncSession, current_user: "User"
    ) -> ModelType:
        object_in_data = object_in.model_dump()

        if "user_id" in object_in_data:
            self._check_user_permission(object_in_data["user_id"], current_user)

        return await self.crud.create(object_in_data, session)

    async def get_by_id(
        self, object_id: int, session: AsyncSession, current_user: "User"
    ) -> ModelType:
        object_db = await self.crud.get_by_id(object_id, session)
        if not object_db:
            raise ObjectNotFound(
                debug=f"{self.model.__name__} with ID {object_id} not found",
            )
        if current_user:
            self._check_ownership(object_db, current_user)
        return object_db

    async def get_filtered(
        self, filter_query, session: AsyncSession, current_user: "User"
    ) -> list[ModelType]:
        filters = filter_query.get_parsed_tags()
        if current_user:
            if current_user.role == RoleEnum.CUSTOMER:
                for user_id in filters.get("user_id", []):
                    self._check_user_permission(user_id, current_user)

                if not filters.get("user_id", []):
                    filters["user_id"] = [current_user.id]

        return await self.crud.get_filtered(
            session=session,
            filters=filters,
            order_by=filter_query.order_by,
            limit=filter_query.limit,
            offset=filter_query.offset,
        )

    async def update(
        self,
        object_id: int,
        object_in: UpdateSchemaType,
        session: AsyncSession,
        current_user: "User",
    ) -> ModelType:
        await self.get_by_id(object_id, session, current_user)
        update_data = object_in.model_dump(exclude_unset=True, exclude_none=True)
        return await self.crud.update(object_id, update_data, session)

    async def delete(
        self, object_id: int, session: AsyncSession, current_user: "User"
    ) -> None:
        object_db = await self.get_by_id(object_id, session, current_user)
        await self.crud.delete(object_db, session)

    @staticmethod
    def _check_user_permission(user_id: int, current_user: "User"):
        if current_user.role == RoleEnum.CUSTOMER and user_id != current_user.id:
            raise ForbiddenAccess(
                message="You can't access object of another user",
                debug=f"user_id={user_id}, current={current_user.id}",
            )

    @staticmethod
    def _check_ownership(obj: ModelType, current_user: "User"):
        if current_user.role == RoleEnum.CUSTOMER and hasattr(obj, "user_id"):
            if obj.user_id != current_user.id:
                raise ForbiddenAccess(
                    message="You don't own this object",
                    debug=f"owner={obj.user_id}, current={current_user.id}",
                )
