from pydantic import BaseModel


class JwtResponse(BaseModel):
    access_token: str
    refresh_token: str
