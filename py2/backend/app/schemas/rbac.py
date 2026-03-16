"""
RBAC 相关的 Pydantic Schema
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from ..models.enums import UserStatus, RoleStatus, PermissionStatus


# ==================== 用户相关 Schema ====================

class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: Optional[str] = Field(None, max_length=100, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    status: UserStatus = Field(default=UserStatus.ACTIVE, description="状态")


class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6, max_length=100, description="密码")

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """验证用户名格式"""
        if not v:
            raise ValueError('用户名不能为空')
        if not v.replace('_', '').isalnum():
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('密码长度不能少于6位')
        return v


class UserUpdate(BaseModel):
    """用户更新模型"""
    email: Optional[str] = Field(None, max_length=100, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    status: Optional[UserStatus] = Field(None, description="状态")


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserWithRoles(UserResponse):
    """包含角色的用户响应模型"""
    roles: List['RoleResponse'] = []

    class Config:
        from_attributes = True


# ==================== 角色相关 Schema ====================

class RoleBase(BaseModel):
    """角色基础模型"""
    role_code: str = Field(..., min_length=2, max_length=50, description="角色编码")
    role_name: str = Field(..., min_length=2, max_length=50, description="角色名称")
    description: Optional[str] = Field(None, description="描述")
    status: RoleStatus = Field(default=RoleStatus.ACTIVE, description="状态")
    sort_order: int = Field(default=0, description="排序")


class RoleCreate(RoleBase):
    """角色创建模型"""

    @field_validator('role_code')
    @classmethod
    def validate_role_code(cls, v):
        """验证角色编码格式"""
        if not v:
            raise ValueError('角色编码不能为空')
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('角色编码只能包含字母、数字、下划线和连字符')
        return v


class RoleUpdate(BaseModel):
    """角色更新模型"""
    role_name: Optional[str] = Field(None, min_length=2, max_length=50, description="角色名称")
    description: Optional[str] = Field(None, description="描述")
    status: Optional[RoleStatus] = Field(None, description="状态")
    sort_order: Optional[int] = Field(None, description="排序")


class RoleResponse(RoleBase):
    """角色响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoleWithPermissions(RoleResponse):
    """包含权限的角色响应模型"""
    permissions: List['PermissionResponse'] = []

    class Config:
        from_attributes = True


# ==================== 权限相关 Schema ====================

class PermissionBase(BaseModel):
    """权限基础模型"""
    permission_code: str = Field(..., min_length=2, max_length=100, description="权限编码")
    permission_name: str = Field(..., min_length=2, max_length=100, description="权限名称")
    resource_type: str = Field(..., description="资源类型")
    resource_id: Optional[int] = Field(None, description="资源ID")
    description: Optional[str] = Field(None, description="描述")
    status: PermissionStatus = Field(default=PermissionStatus.ACTIVE, description="状态")


class PermissionCreate(PermissionBase):
    """权限创建模型"""
    pass


class PermissionUpdate(BaseModel):
    """权限更新模型"""
    permission_name: Optional[str] = Field(None, min_length=2, max_length=100, description="权限名称")
    resource_type: Optional[str] = Field(None, description="资源类型")
    resource_id: Optional[int] = Field(None, description="资源ID")
    description: Optional[str] = Field(None, description="描述")
    status: Optional[PermissionStatus] = Field(None, description="状态")


class PermissionResponse(PermissionBase):
    """权限响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 登录相关 Schema ====================

class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class LoginResponse(BaseModel):
    """登录响应模型"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# 解决前向引用问题
UserWithRoles.model_rebuild()
RoleWithPermissions.model_rebuild()


# ==================== 用户管理相关 Schema ====================

class UserUpdateStatus(BaseModel):
    """用户状态更新模型"""
    status: UserStatus = Field(..., description="状态")


class UserAssignRoles(BaseModel):
    """用户角色分配模型"""
    role_ids: List[int] = Field(..., description="角色ID列表")


# ==================== 角色管理相关 Schema ====================

class RoleUpdateStatus(BaseModel):
    """角色状态更新模型"""
    status: RoleStatus = Field(..., description="状态")


class RoleUpdatePermissions(BaseModel):
    """角色权限更新模型"""
    permission_ids: List[int] = Field(..., description="权限ID列表")
