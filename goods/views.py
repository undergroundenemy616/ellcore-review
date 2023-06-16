from typing import List, Annotated
from goods.models import GoodsIn, GoodsOut, GoodsUpdate
from users.models import User
from users.services import get_current_active_user
from fastapi import Depends
from organizations.services import OrganizationServices
import goods.services as GoodsServices
from typing import List

from fastapi import APIRouter

goods_router = APIRouter(prefix='/goods')


@goods_router.post("", response_model=GoodsOut)
async def create_good(good: GoodsIn,
                      current_user: Annotated[User, Depends(get_current_active_user)]):
  return await GoodsServices.create_good(good, current_user)

@goods_router.get("", response_model=List[GoodsOut])
async def read_good(current_user: Annotated[User, Depends(get_current_active_user)]):
  return await GoodsServices.read_goods(current_user, 0)

@goods_router.get("/all", response_model=List[GoodsOut])
async def read_good(current_user: Annotated[User, Depends(get_current_active_user)]):
  return await GoodsServices.read_goods(current_user, 1)

@goods_router.patch("", response_model=GoodsOut)
async def patch_good(good: GoodsUpdate,
                    current_user: Annotated[User, Depends(get_current_active_user)]):
  return await GoodsServices.patch_good(good, current_user)