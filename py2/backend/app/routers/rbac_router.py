"""
RBAC 管理 API 路由
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..dependencies.auth import get_current_user, require_role
from ..models import User
from ..schemas.rbac import RoleResponse, PermissionResponse
from ..schemas.common import ApiResponse
from ..services import RBACService

# 创建路由器
router = APIRouter(prefix="/api/v1", tags=["RBAC管理"])


@router.get("/users/me/permissions", response_model=ApiResponse[List[str]], summary="获取当前用户权限")
async def get_user_permissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的所有权限编码

    - 需要认证
    """
    rbac_service = RBACService(db)
    permissions = rbac_service.get_user_permissions(current_user.id)

    return ApiResponse(code=200, message="查询成功", data=list(permissions))


@router.get("/users/me/roles", response_model=ApiResponse[List[RoleResponse]], summary="获取当前用户角色")
async def get_user_roles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的所有角色

    - 需要认证
    """
    rbac_service = RBACService(db)
    roles = rbac_service.get_user_roles(current_user.id)

    return ApiResponse(code=200, message="查询成功", data=roles)


@router.post("/users/{user_id}/roles", response_model=ApiResponse, summary="分配用户角色")
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    为指定用户分配角色

    - 需要角色: admin
    """
    rbac_service = RBACService(db)
    success = rbac_service.assign_role_to_user(user_id, role_id)

    if not success:
        return ApiResponse(code=400, message="分配角色失败", data=None)

    return ApiResponse(code=200, message="分配成功", data=None)


@router.delete("/users/{user_id}/roles/{role_id}", response_model=ApiResponse, summary="撤销用户角色")
async def revoke_role_from_user(
    user_id: int,
    role_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    撤销指定用户的角色

    - 需要角色: admin
    """
    rbac_service = RBACService(db)
    success = rbac_service.revoke_role_from_user(user_id, role_id)

    if not success:
        return ApiResponse(code=400, message="撤销角色失败", data=None)

    return ApiResponse(code=200, message="撤销成功", data=None)


@router.post("/roles/{role_id}/permissions", response_model=ApiResponse, summary="分配角色权限")
async def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    为指定角色分配权限

    - 需要角色: admin
    """
    rbac_service = RBACService(db)
    success = rbac_service.assign_permission_to_role(role_id, permission_id)

    if not success:
        return ApiResponse(code=400, message="分配权限失败", data=None)

    return ApiResponse(code=200, message="分配成功", data=None)


@router.delete("/roles/{role_id}/permissions/{permission_id}", response_model=ApiResponse, summary="撤销角色权限")
async def revoke_permission_from_role(
    role_id: int,
    permission_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    撤销指定角色的权限

    - 需要角色: admin
    """
    rbac_service = RBACService(db)
    success = rbac_service.revoke_permission_from_role(role_id, permission_id)

    if not success:
        return ApiResponse(code=400, message="撤销权限失败", data=None)

    return ApiResponse(code=200, message="撤销成功", data=None)
