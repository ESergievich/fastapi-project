from fastapi import APIRouter, Body, Depends, HTTPException, Request, status, Query
from fastapi_users.router.reset import RESET_PASSWORD_RESPONSES
from pydantic import EmailStr

from fastapi_users import exceptions, models, schemas
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode, ErrorModel

from authentication import fastapi_users, authentication_backend
from authentication.dependencies import get_user_manager
from core import settings
from schemas import UserRead, UserCreate

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        # requires_verification=True,
    ),
)


# /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)


# /request-verify-token
# /verify
# router.include_router(
#     router=fastapi_users.get_verify_router(UserRead),
# )


@router.post(
    "/request-verify-token",
    status_code=status.HTTP_202_ACCEPTED,
    name="verify:request-token",
)
async def request_verify_token(
    request: Request,
    email: EmailStr = Body(..., embed=True),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    try:
        user = await user_manager.get_by_email(str(email))
        await user_manager.request_verify(user, request)
    except (
        exceptions.UserNotExists,
        exceptions.UserInactive,
        exceptions.UserAlreadyVerified,
    ):
        pass

    return None


@router.post(
    "/verify",
    response_model=UserRead,
    name="verify:verify",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.VERIFY_USER_BAD_TOKEN: {
                            "summary": "Bad token, not existing user or"
                            "not the e-mail currently set for the user.",
                            "value": {"detail": ErrorCode.VERIFY_USER_BAD_TOKEN},
                        },
                        ErrorCode.VERIFY_USER_ALREADY_VERIFIED: {
                            "summary": "The user is already verified.",
                            "value": {"detail": ErrorCode.VERIFY_USER_ALREADY_VERIFIED},
                        },
                    }
                }
            },
        }
    },
)
async def verify(
    request: Request,
    token: str = Query(...),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    try:
        user = await user_manager.verify(token, request)
        return schemas.model_validate(UserRead, user)
    except (exceptions.InvalidVerifyToken, exceptions.UserNotExists):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
        )
    except exceptions.UserAlreadyVerified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
        )


# /forgot-password
# /reset-password
# router.include_router(
#     router=fastapi_users.get_reset_password_router(),
# )


@router.post(
    "/forgot-password",
    status_code=status.HTTP_202_ACCEPTED,
    name="reset:forgot_password",
)
async def forgot_password(
    request: Request,
    email: EmailStr = Body(..., embed=True),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    try:
        user = await user_manager.get_by_email(str(email))
    except exceptions.UserNotExists:
        return None

    try:
        await user_manager.forgot_password(user, request)
    except exceptions.UserInactive:
        pass

    return None


@router.post(
    "/reset-password",
    name="reset:reset_password",
    responses=RESET_PASSWORD_RESPONSES,
)
async def reset_password(
    request: Request,
    token: str = Query(...),
    password: str = Body(...),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    try:
        await user_manager.reset_password(token, password, request)
    except (
        exceptions.InvalidResetPasswordToken,
        exceptions.UserNotExists,
        exceptions.UserInactive,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.RESET_PASSWORD_BAD_TOKEN,
        )
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.RESET_PASSWORD_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
