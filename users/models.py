from pydantic import BaseModel
from typing import Optional

class UserOut(BaseModel):
    id : int
    username: str
    email: str
    disabled: bool | None = None
    archived: bool | None = None
    permissions: list[int] | None = None

class Meta(BaseModel):
    skip : int | None = 0
    limit : int | None = 0

class UserOut2(BaseModel):
    rows : list[UserOut]
    meta : Meta

class UserIn(BaseModel):
    username: str
    email: str
    disabled: bool | None = False
    archived: bool | None = False
    permissions: list[int] | None = []
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] | None = None
    email: Optional[str] | None = None
    disabled: Optional[bool] | None = None
    archived: Optional[bool] | None = None
    permissions: Optional[list[int]] | None = None
    password: Optional[str] | None = None

class User(BaseModel):
    id : int
    username: str
    email: str
    disabled: bool | None = None
    archived: bool | None = None
    permissions: list[int]| None = None
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str