"""
RBAC 数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
from .enums import UserStatus, RoleStatus, PermissionStatus

# 用户角色关联表（多对多）
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, comment='主键ID'),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='用户ID'),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, comment='角色ID'),
    Column('created_at', DateTime(timezone=True), server_default=func.now(), comment='创建时间'),
    comment='用户角色关联表'
)

# 角色权限关联表（多对多）
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, comment='主键ID'),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=False, comment='角色ID'),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False, comment='权限ID'),
    Column('created_at', DateTime(timezone=True), server_default=func.now(), comment='创建时间'),
    comment='角色权限关联表'
)


class User(Base):
    """用户模型"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    username = Column(String(50), unique=True, nullable=False, index=True, comment='用户名')
    password = Column(String(255), nullable=False, comment='密码（加密）')
    email = Column(String(100), unique=True, nullable=True, index=True, comment='邮箱')
    phone = Column(String(20), unique=True, nullable=True, index=True, comment='手机号')
    nickname = Column(String(50), nullable=True, comment='昵称')
    avatar = Column(String(255), nullable=True, comment='头像URL')
    status = Column(String(20), default=UserStatus.ACTIVE, nullable=False, comment='状态')
    last_login_at = Column(DateTime(timezone=True), nullable=True, comment='最后登录时间')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 关系
    roles = relationship('Role', secondary=user_roles, back_populates='users', lazy='selectin')

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Role(Base):
    """角色模型"""
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    role_code = Column(String(50), unique=True, nullable=False, index=True, comment='角色编码')
    role_name = Column(String(50), nullable=False, comment='角色名称')
    description = Column(Text, nullable=True, comment='描述')
    status = Column(String(20), default=RoleStatus.ACTIVE, nullable=False, comment='状态')
    sort_order = Column(Integer, default=0, nullable=False, comment='排序')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 关系
    users = relationship('User', secondary=user_roles, back_populates='roles', lazy='selectin')
    permissions = relationship('Permission', secondary=role_permissions, back_populates='roles', lazy='selectin')

    def __repr__(self):
        return f"<Role(id={self.id}, role_code='{self.role_code}')>"


class Permission(Base):
    """权限模型"""
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    permission_code = Column(String(100), unique=True, nullable=False, index=True, comment='权限编码')
    permission_name = Column(String(100), nullable=False, comment='权限名称')
    resource_type = Column(String(20), nullable=False, comment='资源类型')
    resource_id = Column(Integer, nullable=True, comment='资源ID')
    description = Column(Text, nullable=True, comment='描述')
    status = Column(String(20), default=PermissionStatus.ACTIVE, nullable=False, comment='状态')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 关系
    roles = relationship('Role', secondary=role_permissions, back_populates='permissions', lazy='selectin')

    def __repr__(self):
        return f"<Permission(id={self.id}, permission_code='{self.permission_code}')>"
