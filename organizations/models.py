from pydantic import BaseModel
from typing import Optional
from users.models import Meta

class OrganizationOut(BaseModel):
    id : int
    name: str
    inn: str
    # standard_token: str | None = None
    # statistics_token: str | None = None
    # advertizing_token: str | None = None
    archived: bool

class OrganizationOut2(BaseModel):
    rows : list[OrganizationOut]
    meta : Meta

class OrganizationIn(BaseModel):
    name: str
    inn: str
    # standard_token: str | None = None
    # statistics_token: str | None = None
    # advertizing_token: str | None = None
    archived: bool | None = False

class OrganizationUpdate(BaseModel):
    name: Optional[str] | None = None
    inn: Optional[str] | None = None
    # standard_token: str | None = None
    # statistics_token: str | None = None
    # advertizing_token: str | None = None
    archived: Optional[bool] | None = None
