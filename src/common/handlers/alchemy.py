from authlib.jose.errors import BadSignatureError, ExpiredTokenError
from fastapi import Request
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status
from starlette.responses import JSONResponse


async def jwt_error_handler(request: Request, exc: BadSignatureError | ExpiredTokenError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Неверный или истекший токен"},
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    error_msg = str(exc)
    error_type = "Client Error"
    status_code = status.HTTP_409_CONFLICT
    if exc.orig and exc.orig.args:
        if "UniqueViolationError" in exc.orig.args[0]:
            error_msg = exc.orig.args[0].split("DETAIL:")[-1].strip()
        elif "ForeignKeyViolationError" in exc.orig.args[0]:
            error_type = "Not found"
            error_msg = exc.orig.args[0].split("DETAIL:")[-1].strip()
            status_code = status.HTTP_404_NOT_FOUND

    return JSONResponse(
        status_code=status_code,
        content={"error": error_type, "detail": error_msg},
    )


async def no_result_found_handler(request: Request, exc: NoResultFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Not found", "detail": "Объект не найден"},
    )
