"""
权限查询 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..core.database import get_db
from ..dependencies.auth import get_current_user
from ..models import User, Permission
from ..schemas.rbac import PermissionResponse
from ..schemas.common import ApiResponse

# 创建路由器
router = APIRouter(prefix="/api/v1/permissions", tags=["权限查询"])


@router.get("", response_model=ApiResponse[List[PermissionResponse]], summary="获取所有权限")
async def get_permissions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取所有权限列表

    - 需要认证
    - 按权限编码排序
    """
    permissions = db.query(Permission).filter(
        Permission.status == 'active'
    ).order_by(Permission.permission_code.asc()).all()

    return ApiResponse(
        code=200,
        message="查询成功",
        data=[PermissionResponse.model_validate(perm) for perm in permissions]
    )


@router.get("/tree", response_model=ApiResponse[List[Dict[str, Any]]], summary="获取权限树")
async def get_permission_tree(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取权限树结构

    - 需要认证
    - 按资源类型分组
    - 按权限编码排序
    """
    permissions = db.query(Permission).filter(
        Permission.status == 'active'
    ).order_by(Permission.permission_code.asc()).all()

    # 按资源类型分组
    tree: Dict[str, List[Dict[str, Any]]] = {}

    for perm in permissions:
        if perm.resource_type not in tree:
            tree[perm.resource_type] = []

        tree[perm.resource_type].append({
            'id': perm.id,
            'permission_code': perm.permission_code,
            'permission_name': perm.permission_name,
            'resource_type': perm.resource_type,
            'resource_id': perm.resource_id,
            'description': perm.description
        })

    # 转换为列表格式
    result = [
        {
            'resource_type': resource_type,
            'permissions': perms
        }
        for resource_type, perms in sorted(tree.items())
    ]

    return ApiResponse(code=200, message="查询成功", data=result)
