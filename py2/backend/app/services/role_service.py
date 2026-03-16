"""
角色服务类
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from ..models import Role, Permission, user_roles
from ..models.enums import RoleStatus
from ..schemas.rbac import RoleCreate, RoleUpdate


class RoleService:
    """角色管理服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_role(self, role_data: RoleCreate) -> Role:
        """
        创建角色

        Args:
            role_data: 角色创建数据

        Returns:
            创建的角色对象

        Raises:
            ValueError: 当角色编码已存在时
        """
        # 验证角色编码唯一性
        existing_role = self.db.query(Role).filter(Role.role_code == role_data.role_code).first()
        if existing_role:
            raise ValueError(f"角色编码 '{role_data.role_code}' 已存在")

        # 创建角色
        role = Role(
            role_code=role_data.role_code,
            role_name=role_data.role_name,
            description=role_data.description,
            status=role_data.status,
            sort_order=role_data.sort_order
        )

        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)

        return role

    def update_role(self, role_id: int, role_data: RoleUpdate) -> Role:
        """
        更新角色信息

        Args:
            role_id: 角色ID
            role_data: 角色更新数据

        Returns:
            更新后的角色对象

        Raises:
            ValueError: 当角色不存在时
        """
        # 获取角色
        role = self.get_role_by_id(role_id)
        if not role:
            raise ValueError(f"角色ID {role_id} 不存在")

        # 更新字段
        update_data = role_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(role, field, value)

        self.db.commit()
        self.db.refresh(role)

        return role

    def delete_role(self, role_id: int) -> bool:
        """
        删除角色

        Args:
            role_id: 角色ID

        Returns:
            True表示删除成功

        Raises:
            ValueError: 当角色不存在或角色正在被使用时
        """
        # 获取角色
        role = self.get_role_by_id(role_id)
        if not role:
            raise ValueError(f"角色ID {role_id} 不存在")

        # 检查角色是否正在被使用
        user_count = self.db.query(func.count(user_roles.c.user_id)).filter(
            user_roles.c.role_id == role_id
        ).scalar()

        if user_count > 0:
            raise ValueError(f"角色 '{role.role_name}' 正在被 {user_count} 个用户使用，无法删除")

        # 删除角色（级联删除权限关联）
        self.db.delete(role)
        self.db.commit()

        return True

    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        """
        根据ID获取角色

        Args:
            role_id: 角色ID

        Returns:
            角色对象，如果不存在则返回None
        """
        return self.db.query(Role).filter(Role.id == role_id).first()

    def get_roles(self, params: dict) -> Tuple[List[Role], int]:
        """
        获取角色列表，支持分页和搜索

        Args:
            params: 查询参数，包含：
                - page: 页码（从1开始）
                - page_size: 每页大小
                - keyword: 搜索关键词（角色编码、角色名称、描述）
                - status: 状态过滤

        Returns:
            (角色列表, 总数)
        """
        page = params.get('page', 1)
        page_size = params.get('page_size', 10)
        keyword = params.get('keyword')
        status = params.get('status')

        # 构建查询
        query = self.db.query(Role)

        # 关键词搜索
        if keyword:
            query = query.filter(
                or_(
                    Role.role_code.like(f'%{keyword}%'),
                    Role.role_name.like(f'%{keyword}%'),
                    Role.description.like(f'%{keyword}%')
                )
            )

        # 状态过滤
        if status:
            query = query.filter(Role.status == status)

        # 获取总数
        total = query.count()

        # 分页
        offset = (page - 1) * page_size
        roles = query.order_by(Role.sort_order.asc(), Role.id.desc()).offset(offset).limit(page_size).all()

        return roles, total

    def update_role_status(self, role_id: int, status: RoleStatus) -> bool:
        """
        更新角色状态

        Args:
            role_id: 角色ID
            status: 新状态

        Returns:
            True表示更新成功

        Raises:
            ValueError: 当角色不存在时
        """
        role = self.get_role_by_id(role_id)
        if not role:
            raise ValueError(f"角色ID {role_id} 不存在")

        role.status = status
        self.db.commit()

        return True

    def update_role_permissions(self, role_id: int, permission_ids: List[int]) -> bool:
        """
        更新角色权限

        Args:
            role_id: 角色ID
            permission_ids: 权限ID列表

        Returns:
            True表示更新成功

        Raises:
            ValueError: 当角色不存在或权限不存在时
        """
        # 获取角色
        role = self.get_role_by_id(role_id)
        if not role:
            raise ValueError(f"角色ID {role_id} 不存在")

        # 验证权限是否存在
        permissions = self.db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        if len(permissions) != len(permission_ids):
            raise ValueError("部分权限不存在")

        # 清除现有权限
        role.permissions.clear()

        # 分配新权限
        role.permissions.extend(permissions)

        self.db.commit()

        return True
