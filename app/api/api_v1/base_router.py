from typing import Type, Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


from core import (
    db_helper,
    UpdateSchemaType,
    ResponseSchemaType,
    CreateSchemaType,
    FiterInSchemaType,
)
from schemas import create_filter_params
from service import BaseService

if TYPE_CHECKING:
    from models import User


def create_base_router(
    service: BaseService,
    create_schema: Type[CreateSchemaType],
    update_schema: Type[UpdateSchemaType],
    response_schema: Type[ResponseSchemaType],
    filter_in_schema: Type[FiterInSchemaType],
    permission_map: dict,
):
    router = APIRouter()

    @router.post(
        "/",
        response_model=response_schema,
        status_code=status.HTTP_201_CREATED,
    )
    async def create_object(
        object_in: create_schema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        current_user: "User" = Depends(permission_map.get("create", lambda: None)),
    ) -> response_schema:
        return await service.create(object_in, session, current_user)

    @router.get(
        "/{object_id}",
        response_model=response_schema,
        status_code=status.HTTP_200_OK,
    )
    async def get_object_by_id(
        object_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        current_user: "User" = Depends(permission_map.get("get", lambda: None)),
    ) -> response_schema:
        return await service.get_by_id(object_id, session, current_user)

    @router.get(
        "/",
        response_model=list[response_schema],
        status_code=status.HTTP_200_OK,
    )
    async def get_filtered(
        filter_query: Annotated[create_filter_params(filter_in_schema), Depends()],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        current_user: "User" = Depends(permission_map.get("get_all", lambda: None)),
    ) -> list[response_schema]:
        return await service.get_filtered(filter_query, session, current_user)

    @router.patch(
        "/{object_id}",
        response_model=response_schema,
        status_code=status.HTTP_200_OK,
    )
    async def update_object(
        object_id: int,
        object_in: update_schema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        current_user: "User" = Depends(permission_map.get("update", lambda: None)),
    ) -> response_schema:
        return await service.update(object_id, object_in, session, current_user)

    @router.delete(
        "/{object_id}",
        status_code=status.HTTP_200_OK,
    )
    async def delete_object(
        object_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        current_user: "User" = Depends(permission_map.get("delete", lambda: None)),
    ) -> dict:
        await service.delete(object_id, session, current_user)
        return {"message": "Deleted successfully"}

    return router
