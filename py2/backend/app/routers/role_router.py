"""
角色管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..dependencies.auth import get_current_user
from ..models import User
from ..schemas.rbac import (
    RoleCreate, RoleUpdate, RoleResponse, RoleWithPermissions,
    RoleUpdateStatus, RoleUpdatePermissions
)
from ..schemas.common import ApiResponse, PageResponse, PageData
from ..services.role_service import RoleService

# 创建路由器
router = APIRouter(prefix="/api/v1/roles", tags=["角色管理"])


@router.post("", response_model=ApiResponse[RoleResponse], summary="创建角色")
async def create_role(
    role_data: RoleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建角色

    - 需要认证
    - 验证角色编码唯一性
    """
    role_service = RoleService(db)

    try:
        role = role_service.create_role(role_data)
        return ApiResponse(code=200, message="创建成功", data=RoleResponse.model_validate(role))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=PageResponse[RoleResponse], summary="获取角色列表")
async def get_roles(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页大小"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    status_filter: Optional[str] = Query(None, description="状态过滤"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取角色列表

    - 需要认证
    - 支持分页
    - 支持关键词搜索（角色编码、角色名称、描述）
    - 支持状态过滤
    """
    role_service = RoleService(db)

    params = {
        'page': page,
        'page_size': page_size,
        'keyword': keyword,
        'status': status_filter
    }

    roles, total = role_service.get_roles(params)

    # 计算总页数
    pages = (total + page_size - 1) // page_size

    page_data = PageData(
        items=[RoleResponse.model_validate(role) for role in roles],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )

    return PageResponse(code=200, message="查询成功", data=page_data)


@router.get("/{role_id}", response_model=ApiResponse[RoleResponse], summary="获取角色详情")
async def get_role(
    role_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取角色详情

    - 需要认证
    """
    role_service = RoleService(db)

    role = role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"角色ID {role_id} 不存在"
        )

    return ApiResponse(code=200, message="查询成功", data=RoleResponse.model_validate(role))


@router.put("/{role_id}", response_model=ApiResponse[RoleResponse], summary="更新角色")
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新角色信息

    - 需要认证
    """
    role_service = RoleService(db)

    try:
        role = role_service.update_role(role_id, role_data)
        return ApiResponse(code=200, message="更新成功", data=RoleResponse.model_validate(role))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{role_id}", response_model=ApiResponse[None], summary="删除角色")
async def delete_role(
    role_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除角色

    - 需要认证
    - 不能删除正在被使用的角色
    """
    role_service = RoleService(db)

    try:
        role_service.delete_role(role_id)
        return ApiResponse(code=200, message="删除成功", data=None)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{role_id}/status", response_model=ApiResponse[RoleResponse], summary="更新角色状态")
async def update_role_status(
    role_id: int,
    status_data: RoleUpdateStatus,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新角色状态

    - 需要认证
    """
    role_service = RoleService(db)

    try:
        role_service.update_role_status(role_id, status_data.status)
        role = role_service.get_role_by_id(role_id)
        return ApiResponse(code=200, message="状态更新成功", data=RoleResponse.model_validate(role))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{role_id}/permissions", response_model=ApiResponse[list], summary="获取角色权限")
async def get_role_permissions(
    role_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取角色的权限列表

    - 需要认证
    """
    role_service = RoleService(db)

    role = role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"角色ID {role_id} 不存在"
        )

    permissions = [
        {
            'id': perm.id,
            'permission_code': perm.permission_code,
            'permission_name': perm.permission_name,
            'resource_type': perm.resource_type,
            'resource_id': perm.resource_id
        }
        for perm in role.permissions
    ]

    return ApiResponse(code=200, message="查询成功", data=permissions)


@router.put("/{role_id}/permissions", response_model=ApiResponse[None], summary="更新角色权限")
async def update_role_permissions(
    role_id: int,
    permission_data: RoleUpdatePermissions,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新角色权限

    - 需要认证
    - 会清除角色现有权限，分配新权限
    """
    role_service = RoleService(db)

    try:
        role_service.update_role_permissions(role_id, permission_data.permission_ids)
        return ApiResponse(code=200, message="权限更新成功", data=None)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
