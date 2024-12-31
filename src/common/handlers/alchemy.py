from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette import status
from starlette.responses import JSONResponse
from fastapi import Request


async def integrity_error_handler(request: Request, exc: IntegrityError):
    error_msg = str(exc)
    error_type = "Client Error"
    status_code = status.HTTP_400_BAD_REQUEST
    if exc.orig and exc.orig.args:
        if 'UniqueViolationError' in exc.orig.args[0]:
            error_msg = exc.orig.args[0].split("DETAIL:")[-1].strip()
        elif 'ForeignKeyViolationError' in exc.orig.args[0]:
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
