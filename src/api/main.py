import fastapi
from sqlalchemy.exc import IntegrityError, NoResultFound
from starlette.middleware.cors import CORSMiddleware

from src.api.router import include_routers
from src.common.handlers.alchemy import integrity_error_handler, no_result_found_handler
from src.containers.container import container


def create_app() -> fastapi.FastAPI:
    origins = [
        "*" # TODO add localhost
    ]
    application = fastapi.FastAPI()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(include_routers())
    application.container = container
    return application


app = create_app()
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(NoResultFound, no_result_found_handler)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=8000, log_level="info")
