"""
枚举类型定义
"""
from enum import Enum


class UserStatus(str, Enum):
    """用户状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"


class RoleStatus(str, Enum):
    """角色状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"


class PermissionStatus(str, Enum):
    """权限状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"


class MenuType(str, Enum):
    """菜单类型枚举"""
    DIRECTORY = "directory"  # 目录
    MENU = "menu"  # 菜单
    BUTTON = "button"  # 按钮


class MenuStatus(str, Enum):
    """菜单状态枚举"""
    ENABLED = "enabled"
    DISABLED = "disabled"


class ResourceType(str, Enum):
    """资源类型枚举"""
    MENU = "menu"
    API = "api"
    BUTTON = "button"
