from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from errors import APIException


def register_exception_handlers(app: FastAPI, debug_mode: bool = False):
    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        error = exc.to_pydantic(debug_mode)
        return JSONResponse(
            status_code=exc.status_code,
            content=error.model_dump(),
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        content = {"detail": "Error in the database"}

        if debug_mode:
            error_detail = exc.args[0].split("DETAIL:  ")[1]
            status_code = status.HTTP_409_CONFLICT
            content = {"detail": error_detail}

        return JSONResponse(
            status_code=status_code,
            content=content,
        )
