from pydantic import BaseModel
from typing import Union

class UserIN(BaseModel):
    username: str
    email: str
    rights: list[str]
    password: str
    disabled: bool


class User(BaseModel):
    id : int
    username: str
    email: str
    rights: list[str]
    # password: str
    disabled: bool

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str