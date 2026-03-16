"""
路由层包
"""

from .auth_router import router as auth_router
from .menu_router import router as menu_router
from .permission_router import router as permission_router
from .rbac_router import router as rbac_router
from .role_router import router as role_router
from .user_router import router as user_router

__all__ = [
    "auth_router",
    "menu_router",
    "permission_router",
    "rbac_router",
    "role_router",
    "user_router",
]
