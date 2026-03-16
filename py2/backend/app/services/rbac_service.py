"""
RBAC 权限管理服务
"""
from typing import List, Set, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models import User, Role, Permission
from ..models.enums import RoleStatus, PermissionStatus
from ..schemas.rbac import RoleResponse, PermissionResponse


class RBACService:
    """RBAC 权限管理服务类"""

    def __init__(self, db: Session):
        self.db = db

    def get_user_permissions(self, user_id: int) -> Set[str]:
        """
        获取用户的所有权限编码

        Args:
            user_id: 用户ID

        Returns:
            权限编码集合
        """
        # 查询用户及其角色
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return set()

        # 收集所有权限编码
        permissions = set()
        for role in user.roles:
            # 只包含激活状态的角色
            if role.status != RoleStatus.ACTIVE:
                continue

            for permission in role.permissions:
                # 只包含激活状态的权限
                if permission.status == PermissionStatus.ACTIVE:
                    permissions.add(permission.permission_code)

        return permissions

    def get_user_roles(self, user_id: int) -> List[RoleResponse]:
        """
        获取用户的所有角色

        Args:
            user_id: 用户ID

        Returns:
            角色列表
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return []

        return [RoleResponse.model_validate(role) for role in user.roles]

    def has_permission(self, user_id: int, permission_code: str) -> bool:
        """
        检查用户是否拥有指定权限

        Args:
            user_id: 用户ID
            permission_code: 权限编码

        Returns:
            是否拥有权限
        """
        permissions = self.get_user_permissions(user_id)
        return permission_code in permissions

    def has_any_permission(self, user_id: int, permission_codes: List[str]) -> bool:
        """
        检查用户是否拥有任意一个权限

        Args:
            user_id: 用户ID
            permission_codes: 权限编码列表

        Returns:
            是否拥有任意权限
        """
        permissions = self.get_user_permissions(user_id)
        return any(code in permissions for code in permission_codes)

    def has_all_permissions(self, user_id: int, permission_codes: List[str]) -> bool:
        """
        检查用户是否拥有所有权限

        Args:
            user_id: 用户ID
            permission_codes: 权限编码列表

        Returns:
            是否拥有所有权限
        """
        permissions = self.get_user_permissions(user_id)
        return all(code in permissions for code in permission_codes)

    def assign_role_to_user(self, user_id: int, role_id: int) -> bool:
        """
        为用户分配角色

        Args:
            user_id: 用户ID
            role_id: 角色ID

        Returns:
            是否分配成功
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        role = self.db.query(Role).filter(Role.id == role_id).first()

        if not user or not role:
            return False

        # 检查是否已经分配
        if role in user.roles:
            return False

        user.roles.append(role)
        self.db.commit()
        return True

    def revoke_role_from_user(self, user_id: int, role_id: int) -> bool:
        """
        撤销用户的角色

        Args:
            user_id: 用户ID
            role_id: 角色ID

        Returns:
            是否撤销成功
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        role = self.db.query(Role).filter(Role.id == role_id).first()

        if not user or not role:
            return False

        # 检查是否已分配
        if role not in user.roles:
            return False

        user.roles.remove(role)
        self.db.commit()
        return True

    def assign_permission_to_role(self, role_id: int, permission_id: int) -> bool:
        """
        为角色分配权限

        Args:
            role_id: 角色ID
            permission_id: 权限ID

        Returns:
            是否分配成功
        """
        role = self.db.query(Role).filter(Role.id == role_id).first()
        permission = self.db.query(Permission).filter(Permission.id == permission_id).first()

        if not role or not permission:
            return False

        # 检查是否已经分配
        if permission in role.permissions:
            return False

        role.permissions.append(permission)
        self.db.commit()
        return True

    def revoke_permission_from_role(self, role_id: int, permission_id: int) -> bool:
        """
        撤销角色的权限

        Args:
            role_id: 角色ID
            permission_id: 权限ID

        Returns:
            是否撤销成功
        """
        role = self.db.query(Role).filter(Role.id == role_id).first()
        permission = self.db.query(Permission).filter(Permission.id == permission_id).first()

        if not role or not permission:
            return False

        # 检查是否已分配
        if permission not in role.permissions:
            return False

        role.permissions.remove(permission)
        self.db.commit()
        return True

    def get_user_menu_tree(self, user_id: int) -> List:
        """
        获取用户有权限的菜单树

        Args:
            user_id: 用户ID

        Returns:
            菜单树列表
        """
        from ..models.menu import Menu
        from ..models.enums import MenuStatus, MenuType

        # 获取用户权限
        permissions = self.get_user_permissions(user_id)

        # 查询所有启用的菜单
        stmt = select(Menu).where(
            Menu.status == MenuStatus.ENABLED
        ).order_by(Menu.sort_order)

        menus = self.db.execute(stmt).scalars().all()

        # 过滤用户有权限的菜单（如果没有权限控制，则返回所有菜单）
        if permissions:
            filtered_menus = []
            for menu in menus:
                # 如果菜单没有权限要求，或者用户有该权限
                if not menu.permission_code or menu.permission_code in permissions:
                    filtered_menus.append(menu)
            menus = filtered_menus

        # 构建菜单树
        return self._build_menu_tree(menus)

    def _build_menu_tree(self, menus: List, parent_id: Optional[int] = None) -> List:
        """
        构建菜单树形结构

        Args:
            menus: 菜单列表
            parent_id: 父菜单ID

        Returns:
            菜单树列表
        """
        from ..schemas.menu import MenuTreeNode

        tree = []
        for menu in menus:
            if menu.parent_id == parent_id:
                # 创建树节点
                node_data = {
                    'id': menu.id,
                    'parent_id': menu.parent_id,
                    'name': menu.name,
                    'icon': menu.icon,
                    'route': menu.route,
                    'component': menu.component,
                    'menu_type': menu.menu_type,
                    'permission_code': menu.permission_code,
                    'sort_order': menu.sort_order,
                    'status': menu.status,
                    'created_at': menu.created_at,
                    'updated_at': menu.updated_at,
                    'children': self._build_menu_tree(menus, menu.id)
                }
                tree.append(node_data)

        return tree
