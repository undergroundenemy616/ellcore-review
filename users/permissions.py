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

"""
Хорошим тоном является инкапсуляция логики, связанной с разрешениями, в отдельный класс. 
Это делает код более структурированным и упрощает повторное использование и тестирование.

Однако, этот класс смешивает две ответственности: он не только проверяет разрешения, 
но и выбрасывает HTTP-исключения при обнаружении проблем. Это нарушает принцип единственной 
ответственности (Single Responsibility Principle, SRP), один из пяти основных принципов SOLID в 
объектно-ориентированном программировании.

Принцип единственной ответственности гласит, что класс должен иметь только одну причину для изменения. 
В данном случае, класс PermissionChecker может изменяться по двум причинам: если изменяется логика 
проверки разрешений или если изменяется способ обработки HTTP-исключений. Это может привести к тому, ч
то класс станет сложнее поддерживать и тестировать.

Вместо этого, было бы лучше, если бы PermissionChecker просто возвращал True или False, в зависимости от того, 
имеет ли пользователь требуемые разрешения. Затем можно было бы обработать эти результаты роутере FastAPI и 
выбросить соответствующие HTTP-исключения там.

"""
class PermissionChecker:
    def __init__(self, required_permissions: list[int]) -> None:
        self.required_permissions = required_permissions
        self.required_permissions.append(1) # Использование магических значений очень не хорошо, мне вот
        # с первого прочтения не очень понятно, почему всегда здесь апендим именно 1.

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
    