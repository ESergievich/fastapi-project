from fastapi_users import FastAPIUsers

from models import User
from .backend import authentication_backend
from .dependencies import get_user_manager

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)
