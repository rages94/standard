from dependency_injector.wiring import inject
from fastapi import APIRouter, Security
from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer, JwtAuthorizationCredentials

from src.config import Settings
from src.domain.jwt.dto.output import JwtResponse

settings = Settings()
token_router = APIRouter()
access_bearer = JwtAccessBearer(secret_key=settings.jwt.secret_key)
refresh_bearer = JwtRefreshBearer(secret_key=settings.jwt.refresh_secret_key)


@token_router.post("/refresh", responses={200: {"model": JwtResponse}})
@inject
async def refresh(
    credentials: JwtAuthorizationCredentials = Security(refresh_bearer)
) -> JwtResponse:
    access_token = access_bearer.create_access_token(subject=credentials.subject)
    refresh_token = refresh_bearer.create_refresh_token(subject=credentials.subject)
    return JwtResponse(access_token=access_token, refresh_token=refresh_token)
