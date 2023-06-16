from typing import List, Annotated
from organizations.models import OrganizationIn, OrganizationOut, OrganizationUpdate
from users.models import User
from users.services import get_current_active_user
from fastapi import Depends
from organizations.services import OrganizationServices
from typing import List

from fastapi import APIRouter

organization_router = APIRouter(prefix='/organization')


@organization_router.post("", response_model=OrganizationOut)
async def create_organization(organization: OrganizationIn,
                              current_user: Annotated[User, Depends(get_current_active_user)]):
    return await OrganizationServices().create_organization(organization, current_user)

@organization_router.put("", response_model=OrganizationOut)
async def update_organization(organization: OrganizationUpdate,
                              current_user: Annotated[User, Depends(get_current_active_user)]):
    return await OrganizationServices().update_organization(organization, current_user)

@organization_router.patch("", response_model=OrganizationOut)
async def update_organization1(organization: OrganizationUpdate,
                              current_user: Annotated[User, Depends(get_current_active_user)]):
    return await OrganizationServices().update_organization(organization, current_user)

@organization_router.get("/all", response_model=List[OrganizationOut])
async def read_organization(current_user: Annotated[User, Depends(get_current_active_user)]):
    return await OrganizationServices().read_organization(current_user, 1)

@organization_router.get("/{id}", response_model=List[OrganizationOut])
async def read_user_dy_id(id: int, current_user: Annotated[User, Depends(get_current_active_user)]):
    return await OrganizationServices().get_organization_by_id(id, current_user)

@organization_router.get("", response_model=List[OrganizationOut])
async def read_organization(current_user: Annotated[User, Depends(get_current_active_user)]):
    return await OrganizationServices().read_organization(current_user, 0)

# @user_router.get("", response_model=List[UserOut])
# async def read_user(current_user: Annotated[User, Depends(get_current_active_user)]):
#     return await UserServices().read_user(current_user, 0)

# @user_router.get("/all", response_model=List[UserOut])
# async def read_user(current_user: Annotated[User, Depends(get_current_active_user)]):
#     return await UserServices().read_user(current_user, 1)