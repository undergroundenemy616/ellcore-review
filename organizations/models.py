from pydantic import BaseModel


class OrganizationOut(BaseModel):
    id : int
    name: str | None = None
    inn: str | None = None
    # standard_token: str | None = None
    # statistics_token: str | None = None
    # advertizing_token: str | None = None
    archived: bool | None = False

class OrganizationIn(BaseModel):
    name: str
    inn: str
    # standard_token: str | None = None
    # statistics_token: str | None = None
    # advertizing_token: str | None = None
    archived: bool | None = False

class OrganizationUpdate(BaseModel):
    id: int
    name: str | None = None
    inn: str | None = None
    # standard_token: str | None = None
    # statistics_token: str | None = None
    # advertizing_token: str | None = None
    archived: bool | None = None
