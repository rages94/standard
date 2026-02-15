from datetime import datetime

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials, JwtRefreshBearer

from src.config import Settings
from src.data.models import User
from src.data.models.auth_link import UserBotLogin
from src.data.models.user import UserCreate, UserLogin, UserPublic, UserUpdate
from src.data.uow import UnitOfWork
from src.domain.auth_link.dto.filters import AuthLinkFilterSchema
from src.domain.bot.use_cases.send_message import BotSendMessage
from src.domain.jwt.dto.output import JwtResponse
from src.domain.user.dto.filters import UserFilterSchema

settings = Settings()
user_router = APIRouter()
access_bearer = JwtAccessBearer(secret_key=settings.jwt.secret_key)
refresh_bearer = JwtRefreshBearer(secret_key=settings.jwt.refresh_secret_key)


@user_router.post("/register/", status_code=201)
@inject
async def register_user(
    body: UserCreate, uow: UnitOfWork = Depends(Provide["repositories.uow"])
) -> UserPublic:
    user = User(
        username=body.username, hashed_password=User.get_password_hash(body.password)
    )
    async with uow:
        existing_user = await uow.user_repo.filter(
            UserFilterSchema(username=body.username).model_dump(exclude_unset=True)
        )
        if existing_user:
            raise HTTPException(
                status_code=400, detail="Пользователь с таким никнеймом уже существует!"
            )
        uow.user_repo.add(user)
        await uow.commit()
        await uow.refresh(user)
    return user


@user_router.post("/login/")
@inject
async def login(
    body: UserLogin, uow: UnitOfWork = Depends(Provide["repositories.uow"])
) -> JwtResponse:
    async with uow:
        existing_user = await uow.user_repo.filter(
            UserFilterSchema(username=body.username).model_dump(exclude_unset=True)
        )
        if not existing_user:
            raise HTTPException(status_code=401, detail="Неверный никнейм или пароль!")
        if not existing_user[0].check_password(body.password):
            raise HTTPException(status_code=401, detail="Неверный никнейм или пароль!")
        access_token = access_bearer.create_access_token(
            subject={"id": str(existing_user[0].id)}
        )
        refresh_token = refresh_bearer.create_refresh_token(
            subject={"id": str(existing_user[0].id)}
        )
        return JwtResponse(access_token=access_token, refresh_token=refresh_token)


@user_router.post("/login/bot/")
@inject
async def bot_login(
    body: UserBotLogin,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    bot_send_message: BotSendMessage = Depends(Provide["use_cases.bot_send_message"]),
) -> JwtResponse:
    async with uow:
        existing_auth_link = await uow.auth_link_repo.filter(
            AuthLinkFilterSchema(
                id=body.token,
                user_id=None,
                expire_datetime_gt=datetime.now(),
            ).model_dump()
        )
        if not existing_auth_link:
            raise HTTPException(status_code=400, detail="Ссылка недействительна!")

        existing_user = await uow.user_repo.filter(
            UserFilterSchema(username=body.username).model_dump(exclude_unset=True)
        )
        if not existing_user:
            raise HTTPException(status_code=401, detail="Неверный никнейм или пароль!")

        user = existing_user[0]
        user_id = user.id
        if not user.check_password(body.password):
            raise HTTPException(status_code=401, detail="Неверный никнейм или пароль!")

        await uow.user_repo.update(dict(id=user_id, telegram_chat_id=body.chat_id))
        await uow.auth_link_repo.update(
            dict(id=existing_auth_link[0].id, user_id=user_id)
        )
        await uow.commit()

        await bot_send_message("Авторизация прошла успешно", body.chat_id)

        access_token = access_bearer.create_access_token(subject={"id": str(user_id)})
        refresh_token = refresh_bearer.create_refresh_token(
            subject={"id": str(user_id)}
        )
        return JwtResponse(access_token=access_token, refresh_token=refresh_token)


@user_router.get("/me/")
@inject
async def get_current_user(
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> UserPublic:
    async with uow:
        return await uow.user_repo.get_one(dict(id=credentials["id"]))


@user_router.patch("/me/")
@inject
async def update_user(
    data: UserUpdate,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> UserPublic:
    async with uow:
        await uow.user_repo.update(
            dict(id=credentials["id"], **data.model_dump(exclude_none=True))
        )
        await uow.commit()
        return await uow.user_repo.get_one(dict(id=credentials["id"]))
