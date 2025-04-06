from typing import TYPE_CHECKING

from fastapi import Depends, HTTPException
from starlette import status

from authentication import current_active_user

if TYPE_CHECKING:
    from models import User
    from utils import RoleEnum


def role_required(*allowed_roles: "RoleEnum"):
    async def verify_role(user: "User" = Depends(current_active_user)):
        if allowed_roles and user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return user

    return verify_role


def superuser_required(user: "User" = Depends(current_active_user)):
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return user
