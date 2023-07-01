from typing import List, Annotated
from goods.models import GoodsIn, GoodsOut, GoodsUpdate, GoodsOut2
from users.models import User
from users.services import get_current_active_user
from fastapi import Depends
import goods.services as GoodsServices
from typing import List

from fastapi import APIRouter

goods_router = APIRouter(prefix='/goods', tags=['goods'])


"""
FastAPI предоставляет удобный способ добавления документации для ваших API-эндпоинтов прямо в декораторах маршрутов.
Вы можете использовать параметры, такие как summary, description, response_description, чтобы добавить информацию о 
конкретном API-маршруте. Вот пример документации для указанного вами роутера:

@goods_router.post("", response_model=GoodsOut,
                   summary="Create a new good",
                   description="This endpoint allows for the creation of a new good. It requires authentication and appropriate permissions.",
                   response_description="The created good")
async def create_good(good: GoodsIn,
                      current_user: Annotated[User, Depends(get_current_active_user)]):
    return await GoodsServices.create_good(good, current_user)
    

Эта документация будет автоматически отображаться в интерфейсе Swagger UI или ReDoc, предоставляемом FastAPI.
 Это делает ваш API более понятным для других разработчиков и пользователей, а также помогает в отладке и тестировании.
"""
@goods_router.post("", response_model=GoodsOut)
async def create_good(good: GoodsIn,
                      current_user: Annotated[User, Depends(get_current_active_user)]):
  return await GoodsServices.create_good(good, current_user)

@goods_router.get("", response_model=GoodsOut2)
async def read_good(current_user: Annotated[User, Depends(get_current_active_user)],
                    skip: int = 0, limit: int | None = 100):
  obj = await GoodsServices.read_goods(current_user, 0, skip, limit)
  return {"rows" : obj, "meta" : {"skip" : skip, "limit" : limit}}

@goods_router.get("/all", response_model=GoodsOut2)
async def read_good(current_user: Annotated[User, Depends(get_current_active_user)],
                    skip: int = 0, limit: int | None = 100):
  obj = await GoodsServices.read_goods(current_user, 1, skip, limit)
  return {"rows" : obj, "meta" : {"skip" : skip, "limit" : limit}}

@goods_router.patch("/{id}", response_model=GoodsOut)
async def patch_good(id: int,
                    good: GoodsUpdate,
                    current_user: Annotated[User, Depends(get_current_active_user)]):
  return await GoodsServices.patch_good(id, good, current_user)

@goods_router.patch("/archive/{id}", response_model=GoodsOut)
async def archive_good(id: int,
                    current_user: Annotated[User, Depends(get_current_active_user)]):
  return await GoodsServices.archive_good(id, current_user)

@goods_router.get("/{id}", response_model=GoodsOut)
async def read_good_by_id(id:int,
                          current_user: Annotated[User, Depends(get_current_active_user)]):
  return await GoodsServices.read_good_by_id(id, current_user)