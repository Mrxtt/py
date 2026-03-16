"""
菜单相关的 Pydantic Schema
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from ..models.enums import MenuType, MenuStatus
import re


# ==================== 菜单相关 Schema ====================

class MenuBase(BaseModel):
    """菜单基础模型"""
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    name: str = Field(..., min_length=1, max_length=100, description="菜单名称")
    icon: Optional[str] = Field(None, max_length=100, description="菜单图标")
    route: Optional[str] = Field(None, max_length=200, description="路由路径")
    component: Optional[str] = Field(None, max_length=200, description="组件路径")
    menu_type: MenuType = Field(default=MenuType.MENU, description="菜单类型")
    permission_code: Optional[str] = Field(None, max_length=100, description="权限编码")
    sort_order: int = Field(default=0, description="排序")
    status: MenuStatus = Field(default=MenuStatus.ENABLED, description="状态")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """验证菜单名称，防止XSS攻击"""
        # 移除HTML标签
        v = re.sub(r'<[^>]+>', '', v)
        # 移除JavaScript代码
        v = re.sub(r'javascript:', '', v, flags=re.IGNORECASE)
        # 移除on事件
        v = re.sub(r'on\w+\s*=', '', v, flags=re.IGNORECASE)
        return v

    @field_validator('route')
    @classmethod
    def validate_route(cls, v):
        """验证路由路径格式"""
        if v:
            # 验证路由格式（以/开头，只包含字母、数字、下划线、连字符、斜杠）
            if not re.match(r'^/[\w\-/]*$', v):
                raise ValueError('路由路径格式不正确，应以/开头，只包含字母、数字、下划线、连字符、斜杠')
        return v


class MenuCreate(MenuBase):
    """菜单创建模型"""
    pass


class MenuUpdate(BaseModel):
    """菜单更新模型"""
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="菜单名称")
    icon: Optional[str] = Field(None, max_length=100, description="菜单图标")
    route: Optional[str] = Field(None, max_length=200, description="路由路径")
    component: Optional[str] = Field(None, max_length=200, description="组件路径")
    menu_type: Optional[MenuType] = Field(None, description="菜单类型")
    permission_code: Optional[str] = Field(None, max_length=100, description="权限编码")
    sort_order: Optional[int] = Field(None, description="排序")
    status: Optional[MenuStatus] = Field(None, description="状态")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """验证菜单名称，防止XSS攻击"""
        if v:
            v = re.sub(r'<[^>]+>', '', v)
            v = re.sub(r'javascript:', '', v, flags=re.IGNORECASE)
            v = re.sub(r'on\w+\s*=', '', v, flags=re.IGNORECASE)
        return v

    @field_validator('route')
    @classmethod
    def validate_route(cls, v):
        """验证路由路径格式"""
        if v:
            if not re.match(r'^/[\w\-/]*$', v):
                raise ValueError('路由路径格式不正确，应以/开头，只包含字母、数字、下划线、连字符、斜杠')
        return v


class MenuResponse(MenuBase):
    """菜单响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MenuTreeNode(MenuResponse):
    """菜单树节点模型"""
    children: List['MenuTreeNode'] = []

    class Config:
        from_attributes = True


# 解决前向引用问题
MenuTreeNode.model_rebuild()
