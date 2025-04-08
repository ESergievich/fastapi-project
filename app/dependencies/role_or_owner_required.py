from typing import TYPE_CHECKING

from fastapi import Path, Depends

from authentication import current_active_user
from errors import ForbiddenAccess
from utils import RoleEnum

if TYPE_CHECKING:
    from models import User


def role_or_owner_required(
    user_id: int = Path(...),
    current_user: "User" = Depends(current_active_user),
) -> "User":
    if current_user.role in [RoleEnum.ADMIN, RoleEnum.MANAGER]:
        return current_user

    if current_user.role == RoleEnum.CUSTOMER and current_user.id == user_id:
        return current_user

    raise ForbiddenAccess(debug=f"user_id={user_id}, current={current_user.id}")
