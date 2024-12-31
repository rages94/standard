from pydantic import BaseModel


class UserFilterSchema(BaseModel):
    username: str | None = None
    email: str | None = None
