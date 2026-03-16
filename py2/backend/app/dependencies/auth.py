"""
认证授权依赖
"""
from typing import Optional, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.security import decode_access_token
from ..models import User
from ..models.enums import UserStatus
from ..services import RBACService

# HTTP Bearer 认证
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户

    Args:
        credentials: HTTP认证凭据
        db: 数据库会话

    Returns:
        当前用户对象

    Raises:
        HTTPException: 认证失败或用户不存在
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 解码JWT令牌
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    # 获取用户ID
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # 查询用户
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    # 检查用户状态
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )

    return user


def require_permission(permission_code: str) -> Callable:
    """
    权限检查依赖工厂函数

    Args:
        permission_code: 需要的权限编码

    Returns:
        依赖函数
    """
    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        """
        检查用户是否拥有指定权限

        Args:
            current_user: 当前用户
            db: 数据库会话

        Returns:
            当前用户

        Raises:
            HTTPException: 权限不足
        """
        rbac_service = RBACService(db)

        if not rbac_service.has_permission(current_user.id, permission_code):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"缺少权限: {permission_code}"
            )

        return current_user

    return permission_checker


def require_any_permission(permission_codes: list) -> Callable:
    """
    多权限检查依赖工厂函数（拥有任意权限即可）

    Args:
        permission_codes: 权限编码列表

    Returns:
        依赖函数
    """
    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        """
        检查用户是否拥有任意一个权限

        Args:
            current_user: 当前用户
            db: 数据库会话

        Returns:
            当前用户

        Raises:
            HTTPException: 权限不足
        """
        rbac_service = RBACService(db)

        if not rbac_service.has_any_permission(current_user.id, permission_codes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"缺少权限，需要以下任意权限: {', '.join(permission_codes)}"
            )

        return current_user

    return permission_checker


def require_all_permissions(permission_codes: list) -> Callable:
    """
    多权限检查依赖工厂函数（需要拥有所有权限）

    Args:
        permission_codes: 权限编码列表

    Returns:
        依赖函数
    """
    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        """
        检查用户是否拥有所有权限

        Args:
            current_user: 当前用户
            db: 数据库会话

        Returns:
            当前用户

        Raises:
            HTTPException: 权限不足
        """
        rbac_service = RBACService(db)

        if not rbac_service.has_all_permissions(current_user.id, permission_codes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"缺少权限，需要以下所有权限: {', '.join(permission_codes)}"
            )

        return current_user

    return permission_checker


def require_role(role_code: str) -> Callable:
    """
    角色检查依赖工厂函数

    Args:
        role_code: 需要的角色编码

    Returns:
        依赖函数
    """
    def role_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        """
        检查用户是否拥有指定角色

        Args:
            current_user: 当前用户
            db: 数据库会话

        Returns:
            当前用户

        Raises:
            HTTPException: 角色不足
        """
        rbac_service = RBACService(db)
        roles = rbac_service.get_user_roles(current_user.id)

        role_codes = [role.role_code for role in roles]

        if role_code not in role_codes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"缺少角色: {role_code}"
            )

        return current_user

    return role_checker


def require_any_role(role_codes: list) -> Callable:
    """
    多角色检查依赖工厂函数（拥有任意角色即可）

    Args:
        role_codes: 角色编码列表

    Returns:
        依赖函数
    """
    def role_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        """
        检查用户是否拥有任意一个角色

        Args:
            current_user: 当前用户
            db: 数据库会话

        Returns:
            当前用户

        Raises:
            HTTPException: 角色不足
        """
        rbac_service = RBACService(db)
        roles = rbac_service.get_user_roles(current_user.id)

        user_role_codes = [role.role_code for role in roles]

        if not any(role_code in user_role_codes for role_code in role_codes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"缺少角色，需要以下任意角色: {', '.join(role_codes)}"
            )

        return current_user

    return role_checker
