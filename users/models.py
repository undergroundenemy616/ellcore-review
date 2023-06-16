from pydantic import BaseModel
from typing import Optional


class UserOut(BaseModel):
    id : int
    username: str
    email: str
    disabled: bool | None = None
    archived: bool | None = None
    permissions: list[str] | None = None

class UserIn(BaseModel):
    username: str
    email: str
    disabled: bool | None = False
    archived: bool | None = False
    permissions: list[str]| None = []
    password: str

class UserUpdate(BaseModel):
    id: int
    username: Optional[str] | None = None
    email: Optional[str] | None = None
    disabled: Optional[bool] | None = None
    archived: Optional[bool] | None = None
    permissions: Optional[list[str]] | None = None
    password: Optional[str] | None = None

class User(BaseModel):
    id : int
    username: str
    email: str
    disabled: bool | None = None
    archived: bool | None = None
    permissions: list[str]| None = None
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str