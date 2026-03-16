"""
菜单数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
from .enums import MenuType, MenuStatus


class Menu(Base):
    """菜单模型"""
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    parent_id = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'), nullable=True, index=True, comment='父菜单ID')
    name = Column(String(100), nullable=False, comment='菜单名称')
    icon = Column(String(100), nullable=True, comment='菜单图标')
    route = Column(String(200), nullable=True, comment='路由路径')
    component = Column(String(200), nullable=True, comment='组件路径')
    menu_type = Column(String(20), default=MenuType.MENU, nullable=False, comment='菜单类型')
    permission_code = Column(String(100), nullable=True, index=True, comment='权限编码')
    sort_order = Column(Integer, default=0, nullable=False, comment='排序')
    status = Column(String(20), default=MenuStatus.ENABLED, nullable=False, comment='状态')
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment='更新时间')

    # 自引用关系（父子菜单）
    parent = relationship('Menu', remote_side=[id], back_populates='children')
    children = relationship('Menu', back_populates='parent', cascade='all, delete-orphan', order_by='Menu.sort_order')

    def __repr__(self):
        return f"<Menu(id={self.id}, name='{self.name}', parent_id={self.parent_id})>"
