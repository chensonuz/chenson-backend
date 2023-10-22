import traceback

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.exceptions import classes as ex
from core.schemas.base import APIResponse


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(ex.UnprocessableEntityError)
    async def unproccesable_exception_handler(
        request: Request, exc: ex.UnprocessableEntityError
    ):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(exc.name),
        )

    @app.exception_handler(ex.APIException)
    async def api_exception_handler(request: Request, exc: ex.APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(exc.detail),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(
                APIResponse(success=False, message=exc.detail)
            ),
        )

    @app.exception_handler(ex.NotFoundError)
    async def not_found_exception_handler(
        request: Request,
        exc: ex.NotFoundError,
        status_code: status = status.HTTP_404_NOT_FOUND,
    ):
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(exc.name),
        )

    @app.exception_handler(ex.ConflictError)
    async def conflict_exception_handler(
        request: Request,
        exc: ex.ConflictError,
        status_code: status = status.HTTP_409_CONFLICT,
    ):
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(exc.name),
        )

    @app.exception_handler(ex.UnauthorizedError)
    async def unauthorized_exception_handler(
        request: Request,
        exc: ex.UnauthorizedError,
        status_code: status = status.HTTP_401_UNAUTHORIZED,
    ):
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(exc.response),
        )

    @app.exception_handler(ex.ValuePydanticError)
    async def value_error_exception_handler(
        request: Request,
        exc: ex.ValuePydanticError,
        status_code: status = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(exc.response),
        )

    @app.exception_handler(ex.ForbiddenError)
    async def forbidden_error_exception_handler(
        request: Request,
        exc: ex.ForbiddenError,
        status_code: status = status.HTTP_403_FORBIDDEN,
    ):
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(exc.name),
        )

    @app.exception_handler(ex.RequestError)
    async def handle_request_error(
        request: Request,
        exc: ex.RequestError,
        status_code: status = status.HTTP_424_FAILED_DEPENDENCY,
    ):
        return JSONResponse(
            status_code=status_code, content=jsonable_encoder(exc.name)
        )

    @app.exception_handler(ex.InternalError)
    async def handle_internal_error(
        request: Request,
        exc: ex.InternalError,
        status_code: status = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        return JSONResponse(
            status_code=status_code, content=jsonable_encoder(exc.name)
        )

    @app.exception_handler(ex.IntegrationError)
    async def handle_503(
        request: Request,
        exc: ex.IntegrationError,
        status_code: status = status.HTTP_503_SERVICE_UNAVAILABLE,
    ):
        return JSONResponse(
            status_code=status_code, content=jsonable_encoder(exc.name)
        )

    @app.exception_handler(Exception)
    def handle_500(
        request: Request,
        exc: Exception,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        # err_msg = {
        #     "message": "Internal Server Error"
        #     if not AppConfig.DEBUG
        #     else traceback.format_exception(exc)[-1].strip(),
        #     "codeError": "internalError",
        # }
        lines = traceback.format_exception(exc)[-1].replace("\n", "")
        err_msg = {
            "message": [line.strip() for line in lines],
            "codeError": "internalError",
        }
        logger.error(err_msg)
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(err_msg),
        )
