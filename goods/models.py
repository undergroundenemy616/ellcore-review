from pydantic import BaseModel
from typing import Optional


class GoodsOut(BaseModel):
    id : int
    article_wb: str
    article_id: int
    manager_id: int
    zero_cost: float
    average_price: float
    optimal_price: float
    organization_id: int
    category_id: int
    archived: bool

class GoodsUpdate(BaseModel):
    id : int
    article_wb: Optional[str] | None = None
    article_id: Optional[int] | None = None
    manager_id: Optional[int] | None = None
    zero_cost: Optional[float] | None = None
    average_price: Optional[float] | None = None
    optimal_price: Optional[float] | None = None
    organization_id: Optional[int] | None = None
    category_id: Optional[int] | None = None
    archived: Optional[bool] | None = None

class GoodsIn(BaseModel):
    article_wb: str
    article_id: int
    manager_id: int
    zero_cost: Optional[float] | None = 0
    average_price: Optional[float] | None = 0
    optimal_price: Optional[float] | None = 0
    organization_id: int
    category_id: int
    archived: Optional[bool] | None = False