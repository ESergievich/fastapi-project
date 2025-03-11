import os

from dotenv import load_dotenv
from fastapi_users.jwt import generate_jwt

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../app/.env"))


def create_verify_token(user):
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "aud": "fastapi-users:verify",
    }
    token = generate_jwt(
        token_data,
        os.getenv("APP_CONFIG__ACCESS_TOKEN__VERIFICATION_TOKEN_SECRET"),
        3600,
    )
    return token
