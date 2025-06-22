from pydantic import BaseModel


class AuthOutput(BaseModel):
    status: str
