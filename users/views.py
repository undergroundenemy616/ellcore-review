from typing import List, Annotated
from users.models import User, UserOut, Token, UserIn, UserUpdate
from users.services import get_current_active_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from users.services import UserServices
from typing import List

from fastapi import APIRouter


user_router = APIRouter(prefix='/user')
token_router = APIRouter(prefix='/token')


@user_router.post("", response_model=UserOut)
async def create_user(user: UserIn, current_user: Annotated[User, Depends(get_current_active_user)]):
    return await UserServices().create_user(user, current_user)

@user_router.patch("", response_model=UserOut)
async def update_user(user: UserUpdate, current_user: Annotated[User, Depends(get_current_active_user)]):
    return await UserServices().update_user(user, current_user)

@user_router.get("", response_model=List[UserOut])
async def read_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return await UserServices().read_user(current_user, 0)

@user_router.get("/all", response_model=List[UserOut])
async def read_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return await UserServices().read_user(current_user, 1)

@user_router.get("/{id}", response_model=UserOut)
async def read_user_dy_id(id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    return await UserServices().read_user_by_id(id, current_user)

# @user_router.get("/{id}/disable", response_model=List[UserOut])
# async def disable_user_dy_id(id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
#     return await UserServices().read_user_by_id(id, current_user)

# @user_router.get("/{id}/archive", response_model=List[UserOut])
# async def archive_user_dy_id(id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
#     return await UserServices().read_user_by_id(id, current_user)

@user_router.post("/me", response_model=UserOut)
async def read_users_me(current_user: Annotated[UserOut, Depends(get_current_active_user)]):
    return current_user

@token_router.post("", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await UserServices().login_for_access_token(form_data)