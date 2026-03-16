"""
用户服务类
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..models import User, Role
from ..models.enums import UserStatus
from ..schemas.rbac import UserCreate, UserUpdate
from ..core.security import get_password_hash


class UserService:
    """用户管理服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        """
        创建用户

        Args:
            user_data: 用户创建数据

        Returns:
            创建的用户对象

        Raises:
            ValueError: 当用户名、邮箱或手机号已存在时
        """
        # 验证用户名唯一性
        existing_user = self.db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise ValueError(f"用户名 '{user_data.username}' 已存在")

        # 验证邮箱唯一性
        if user_data.email:
            existing_email = self.db.query(User).filter(User.email == user_data.email).first()
            if existing_email:
                raise ValueError(f"邮箱 '{user_data.email}' 已存在")

        # 验证手机号唯一性
        if user_data.phone:
            existing_phone = self.db.query(User).filter(User.phone == user_data.phone).first()
            if existing_phone:
                raise ValueError(f"手机号 '{user_data.phone}' 已存在")

        # 创建用户
        user = User(
            username=user_data.username,
            password=get_password_hash(user_data.password),
            email=user_data.email,
            phone=user_data.phone,
            nickname=user_data.nickname,
            avatar=user_data.avatar,
            status=user_data.status
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """
        更新用户信息

        Args:
            user_id: 用户ID
            user_data: 用户更新数据

        Returns:
            更新后的用户对象

        Raises:
            ValueError: 当用户不存在或邮箱、手机号已存在时
        """
        # 获取用户
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"用户ID {user_id} 不存在")

        # 验证邮箱唯一性（排除自己）
        if user_data.email and user_data.email != user.email:
            existing_email = self.db.query(User).filter(
                User.email == user_data.email,
                User.id != user_id
            ).first()
            if existing_email:
                raise ValueError(f"邮箱 '{user_data.email}' 已存在")

        # 验证手机号唯一性（排除自己）
        if user_data.phone and user_data.phone != user.phone:
            existing_phone = self.db.query(User).filter(
                User.phone == user_data.phone,
                User.id != user_id
            ).first()
            if existing_phone:
                raise ValueError(f"手机号 '{user_data.phone}' 已存在")

        # 更新字段
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)

        return user

    def delete_user(self, user_id: int, current_user_id: int) -> bool:
        """
        删除用户

        Args:
            user_id: 要删除的用户ID
            current_user_id: 当前登录用户ID

        Returns:
            True表示删除成功

        Raises:
            ValueError: 当用户不存在或尝试删除当前登录用户时
        """
        # 验证不能删除当前登录用户
        if user_id == current_user_id:
            raise ValueError("不能删除当前登录用户")

        # 获取用户
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"用户ID {user_id} 不存在")

        # 删除用户（级联删除角色关联）
        self.db.delete(user)
        self.db.commit()

        return True

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        根据ID获取用户

        Args:
            user_id: 用户ID

        Returns:
            用户对象，如果不存在则返回None
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_users(self, params: dict) -> Tuple[List[User], int]:
        """
        获取用户列表，支持分页和搜索

        Args:
            params: 查询参数，包含：
                - page: 页码（从1开始）
                - page_size: 每页大小
                - keyword: 搜索关键词（用户名、邮箱、手机号、昵称）
                - status: 状态过滤

        Returns:
            (用户列表, 总数)
        """
        page = params.get('page', 1)
        page_size = params.get('page_size', 10)
        keyword = params.get('keyword')
        status = params.get('status')

        # 构建查询
        query = self.db.query(User)

        # 关键词搜索
        if keyword:
            query = query.filter(
                or_(
                    User.username.like(f'%{keyword}%'),
                    User.email.like(f'%{keyword}%'),
                    User.phone.like(f'%{keyword}%'),
                    User.nickname.like(f'%{keyword}%')
                )
            )

        # 状态过滤
        if status:
            query = query.filter(User.status == status)

        # 获取总数
        total = query.count()

        # 分页
        offset = (page - 1) * page_size
        users = query.order_by(User.id.desc()).offset(offset).limit(page_size).all()

        return users, total

    def update_user_status(self, user_id: int, status: UserStatus) -> bool:
        """
        更新用户状态

        Args:
            user_id: 用户ID
            status: 新状态

        Returns:
            True表示更新成功

        Raises:
            ValueError: 当用户不存在时
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"用户ID {user_id} 不存在")

        user.status = status
        self.db.commit()

        return True

    def assign_roles(self, user_id: int, role_ids: List[int]) -> bool:
        """
        为用户分配角色

        Args:
            user_id: 用户ID
            role_ids: 角色ID列表

        Returns:
            True表示分配成功

        Raises:
            ValueError: 当用户不存在或角色不存在时
        """
        # 获取用户
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"用户ID {user_id} 不存在")

        # 验证角色是否存在
        roles = self.db.query(Role).filter(Role.id.in_(role_ids)).all()
        if len(roles) != len(role_ids):
            raise ValueError("部分角色不存在")

        # 清除现有角色
        user.roles.clear()

        # 分配新角色
        user.roles.extend(roles)

        self.db.commit()

        return True
