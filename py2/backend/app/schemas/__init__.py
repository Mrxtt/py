"""
Schema 包
"""
from .common import ApiResponse, PageResponse, PageData, ErrorResponse
from .rbac import (
    UserBase, UserCreate, UserUpdate, UserResponse, UserWithRoles,
    RoleBase, RoleCreate, RoleUpdate, RoleResponse, RoleWithPermissions,
    PermissionBase, PermissionCreate, PermissionUpdate, PermissionResponse,
    LoginRequest, LoginResponse
)
from .menu import MenuBase, MenuCreate, MenuUpdate, MenuResponse, MenuTreeNode

__all__ = [
    # 通用
    'ApiResponse',
    'PageResponse',
    'PageData',
    'ErrorResponse',

    # 用户
    'UserBase',
    'UserCreate',
    'UserUpdate',
    'UserResponse',
    'UserWithRoles',

    # 角色
    'RoleBase',
    'RoleCreate',
    'RoleUpdate',
    'RoleResponse',
    'RoleWithPermissions',

    # 权限
    'PermissionBase',
    'PermissionCreate',
    'PermissionUpdate',
    'PermissionResponse',

    # 登录
    'LoginRequest',
    'LoginResponse',

    # 菜单
    'MenuBase',
    'MenuCreate',
    'MenuUpdate',
    'MenuResponse',
    'MenuTreeNode',
]
