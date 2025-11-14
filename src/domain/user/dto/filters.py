from pydantic import BaseModel


class UserFilterSchema(BaseModel):
    username: str | None = None
    email: str | None = None
    chat_id: int | None = None
    chat_id_ne: int | None = None
