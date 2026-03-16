"""
用户管理 API 路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..core.database import get_db
from ..dependencies.auth import get_current_user
from ..models import User
from ..schemas.rbac import (
    UserCreate, UserUpdate, UserResponse, UserWithRoles,
    UserUpdateStatus, UserAssignRoles
)
from ..schemas.common import ApiResponse, PageResponse, PageData
from ..services.user_service import UserService

# 创建路由器
router = APIRouter(prefix="/api/v1/users", tags=["用户管理"])


@router.post("", response_model=ApiResponse[UserResponse], summary="创建用户")
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建用户

    - 需要认证
    - 验证用户名、邮箱、手机号唯一性
    - 密码自动加密
    """
    user_service = UserService(db)

    try:
        user = user_service.create_user(user_data)
        return ApiResponse(code=200, message="创建成功", data=UserResponse.model_validate(user))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=PageResponse[UserResponse], summary="获取用户列表")
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页大小"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    status_filter: Optional[str] = Query(None, description="状态过滤"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户列表

    - 需要认证
    - 支持分页
    - 支持关键词搜索（用户名、邮箱、手机号、昵称）
    - 支持状态过滤
    """
    user_service = UserService(db)

    params = {
        'page': page,
        'page_size': page_size,
        'keyword': keyword,
        'status': status_filter
    }

    users, total = user_service.get_users(params)

    # 计算总页数
    pages = (total + page_size - 1) // page_size

    page_data = PageData(
        items=[UserResponse.model_validate(user) for user in users],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )

    return PageResponse(code=200, message="查询成功", data=page_data)


@router.get("/{user_id}", response_model=ApiResponse[UserResponse], summary="获取用户详情")
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户详情

    - 需要认证
    """
    user_service = UserService(db)

    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户ID {user_id} 不存在"
        )

    return ApiResponse(code=200, message="查询成功", data=UserResponse.model_validate(user))


@router.put("/{user_id}", response_model=ApiResponse[UserResponse], summary="更新用户")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新用户信息

    - 需要认证
    - 验证邮箱、手机号唯一性
    """
    user_service = UserService(db)

    try:
        user = user_service.update_user(user_id, user_data)
        return ApiResponse(code=200, message="更新成功", data=UserResponse.model_validate(user))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", response_model=ApiResponse[None], summary="删除用户")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除用户

    - 需要认证
    - 不能删除当前登录用户
    """
    user_service = UserService(db)

    try:
        user_service.delete_user(user_id, current_user.id)
        return ApiResponse(code=200, message="删除成功", data=None)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{user_id}/status", response_model=ApiResponse[UserResponse], summary="更新用户状态")
async def update_user_status(
    user_id: int,
    status_data: UserUpdateStatus,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新用户状态

    - 需要认证
    """
    user_service = UserService(db)

    try:
        user_service.update_user_status(user_id, status_data.status)
        user = user_service.get_user_by_id(user_id)
        return ApiResponse(code=200, message="状态更新成功", data=UserResponse.model_validate(user))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{user_id}/roles", response_model=ApiResponse[list], summary="获取用户角色")
async def get_user_roles(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户的角色列表

    - 需要认证
    """
    user_service = UserService(db)

    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户ID {user_id} 不存在"
        )

    roles = [{'id': role.id, 'role_code': role.role_code, 'role_name': role.role_name}
             for role in user.roles]

    return ApiResponse(code=200, message="查询成功", data=roles)


@router.post("/{user_id}/roles", response_model=ApiResponse[None], summary="分配用户角色")
async def assign_user_roles(
    user_id: int,
    role_data: UserAssignRoles,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    为用户分配角色

    - 需要认证
    - 会清除用户现有角色，分配新角色
    """
    user_service = UserService(db)

    try:
        user_service.assign_roles(user_id, role_data.role_ids)
        return ApiResponse(code=200, message="角色分配成功", data=None)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
