from typing import TYPE_CHECKING

from fastapi import Depends

from authentication import current_active_user
from errors import ForbiddenAccess

if TYPE_CHECKING:
    from models import User
    from utils import RoleEnum


def role_required(*allowed_roles: "RoleEnum"):
    async def verify_role(user: "User" = Depends(current_active_user)):
        if allowed_roles and user.role not in allowed_roles:
            raise ForbiddenAccess(
                debug=f"allowed_roles={allowed_roles}, current={user.role}"
            )
        return user

    return verify_role


def superuser_required(user: "User" = Depends(current_active_user)):
    if not user.is_superuser:
        raise ForbiddenAccess(debug=f"is_superuser=True, current={user.is_superuser}")
    return user
