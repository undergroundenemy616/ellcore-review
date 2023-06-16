from fastapi import HTTPException, status

class PermissionChecker:
    def __init__(self, required_permissions: list[str]) -> None:
        self.required_permissions = required_permissions
        self.required_permissions.append("admin")

    def check_permission(self, permissions: list[str]):
        if permissions == None:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f'Wrong Permissions, required: {self.required_permissions}')
        for r_perm in permissions:
            if (r_perm not in self.required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f'Wrong Permissions, required: {self.required_permissions}')
    
class PermissionValidator:
    def __init__(self) -> None:
        self.permissions = ["admin",
                            "goods.read", "goods.create", "goods.delete",
                            "organizations.read", "organizations.create", "organizations.delete",]
    def validate_permissions(self, permissions: list[str]):
        if permissions != None:
            for r_perm in permissions:
                if r_perm not in self.permissions:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'Incorrect type of permissions: avaliable permissions:{self.permissions}'
                    )
    