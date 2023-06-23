from fastapi import HTTPException, status
from enum import Enum

class Permission(Enum):
    ADMIN = 1
    GOODS_READ = 2
    GOODS_CREATE = 3
    GOODS_DELETE = 4
    ORGANIZATIONS_READ = 5
    ORGANIZATIONS_CREATE = 6
    ORGANIZATIONS_DELETE = 7
    MANAGER_READ = 8
    MANAGER_CREATE = 9
    MANAGER_DELETE = 10
    CATEGORY_READ = 11
    CATEGORY_CREATE = 12
    CATEGORY_DELETE = 13

class PermissionChecker:
    def __init__(self, required_permissions: list[int]) -> None:
        self.required_permissions = required_permissions
        self.required_permissions.append(1)

    def check_permission(self, permissions: list[int]):
        if permissions == None:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f'Wrong Permissions, required: {self.required_permissions}')
        for r_perm in permissions:
            if r_perm in self.required_permissions:
                return
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Wrong Permissions, required: {self.required_permissions}')

def validate_permissions(permissions: list[int]):
    if permissions != None:
        for r_perm in permissions:
            for all_perm in Permission:
                if r_perm == all_perm.value:
                    return
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Incorrect type of permissions'
    )
    