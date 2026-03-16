"""
菜单管理服务
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from ..models.menu import Menu
from ..models.enums import MenuStatus
from ..schemas.menu import MenuCreate, MenuUpdate, MenuResponse, MenuTreeNode


class MenuService:
    """菜单管理服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_menu(self, menu_data: MenuCreate) -> MenuResponse:
        """
        创建新菜单

        Args:
            menu_data: 菜单创建数据

        Returns:
            创建的菜单
        """
        # 验证父菜单是否存在
        if menu_data.parent_id is not None:
            parent_menu = self.db.query(Menu).filter(Menu.id == menu_data.parent_id).first()
            if not parent_menu:
                raise ValueError("父菜单不存在")

        # 验证同级菜单名称唯一性
        self._validate_name_unique(menu_data.name, menu_data.parent_id)

        # 创建菜单
        menu = Menu(**menu_data.model_dump())
        self.db.add(menu)
        self.db.commit()
        self.db.refresh(menu)

        return MenuResponse.model_validate(menu)

    def update_menu(self, menu_id: int, menu_data: MenuUpdate) -> MenuResponse:
        """
        更新菜单信息

        Args:
            menu_id: 菜单ID
            menu_data: 菜单更新数据

        Returns:
            更新后的菜单
        """
        menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise ValueError("菜单不存在")

        # 更新父菜单时，验证循环引用
        if menu_data.parent_id is not None:
            if menu_data.parent_id != menu.parent_id:
                self._validate_no_circular_reference(menu_id, menu_data.parent_id)

        # 更新同级菜单名称唯一性
        if menu_data.name is not None and menu_data.name != menu.name:
            self._validate_name_unique(menu_data.name, menu_data.parent_id, exclude_id=menu_id)

        # 更新菜单
        update_data = menu_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(menu, field, value)

        self.db.commit()
        self.db.refresh(menu)

        return MenuResponse.model_validate(menu)

    def delete_menu(self, menu_id: int) -> bool:
        """
        删除菜单（级联删除子菜单）

        Args:
            menu_id: 菜单ID

        Returns:
            是否删除成功
        """
        menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            return False

        # 级联删除会自动处理子菜单（在模型中配置了 cascade='all, delete-orphan'）
        self.db.delete(menu)
        self.db.commit()

        return True

    def get_menu_by_id(self, menu_id: int) -> Optional[MenuResponse]:
        """
        根据ID获取菜单

        Args:
            menu_id: 菜单ID

        Returns:
            菜单信息
        """
        menu = self.db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            return None

        return MenuResponse.model_validate(menu)

    def get_menus(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[MenuStatus] = None,
        menu_type: Optional[str] = None,
        parent_id: Optional[int] = None
    ) -> tuple[List[MenuResponse], int]:
        """
        获取菜单列表（支持分页和过滤）

        Args:
            skip: 跳过记录数
            limit: 返回记录数
            status: 状态过滤
            menu_type: 菜单类型过滤
            parent_id: 父菜单ID过滤

        Returns:
            菜单列表和总数
        """
        query = self.db.query(Menu)

        # 应用过滤条件
        if status is not None:
            query = query.filter(Menu.status == status)
        if menu_type is not None:
            query = query.filter(Menu.menu_type == menu_type)
        if parent_id is not None:
            query = query.filter(Menu.parent_id == parent_id)

        # 获取总数
        total = query.count()

        # 分页查询
        menus = query.order_by(Menu.sort_order).offset(skip).limit(limit).all()

        return [MenuResponse.model_validate(menu) for menu in menus], total

    def get_menu_tree(self, status: Optional[MenuStatus] = None) -> List:
        """
        获取完整菜单树

        Args:
            status: 状态过滤

        Returns:
            菜单树列表
        """
        query = self.db.query(Menu)

        # 应用过滤条件
        if status is not None:
            query = query.filter(Menu.status == status)

        # 获取所有菜单
        menus = query.order_by(Menu.sort_order).all()

        # 构建菜单树
        return self._build_menu_tree(menus)

    def get_menu_children(self, menu_id: int) -> List[MenuResponse]:
        """
        获取子菜单

        Args:
            menu_id: 父菜单ID

        Returns:
            子菜单列表
        """
        menus = self.db.query(Menu).filter(
            Menu.parent_id == menu_id
        ).order_by(Menu.sort_order).all()

        return [MenuResponse.model_validate(menu) for menu in menus]

    def _validate_name_unique(self, name: str, parent_id: Optional[int], exclude_id: Optional[int] = None):
        """
        验证同级菜单名称唯一性

        Args:
            name: 菜单名称
            parent_id: 父菜单ID
            exclude_id: 排除的菜单ID（用于更新时）

        Raises:
            ValueError: 如果名称已存在
        """
        query = self.db.query(Menu).filter(
            and_(
                Menu.name == name,
                Menu.parent_id == parent_id
            )
        )

        # 更新时排除自身
        if exclude_id is not None:
            query = query.filter(Menu.id != exclude_id)

        existing_menu = query.first()
        if existing_menu:
            raise ValueError(f"同级菜单名称 '{name}' 已存在")

    def _validate_no_circular_reference(self, menu_id: int, new_parent_id: int):
        """
        验证不会形成循环引用

        Args:
            menu_id: 当前菜单ID
            new_parent_id: 新的父菜单ID

        Raises:
            ValueError: 如果会形成循环引用
        """
        # 不能将自己设置为父菜单
        if menu_id == new_parent_id:
            raise ValueError("不能将菜单设置为自己的子菜单")

        # 递归检查新父菜单的祖先菜单，确保不包含当前菜单
        visited = set()
        current_id = new_parent_id

        while current_id is not None:
            if current_id == menu_id:
                raise ValueError("不能形成循环引用")

            if current_id in visited:
                raise ValueError("检测到循环引用")

            visited.add(current_id)

            parent_menu = self.db.query(Menu).filter(Menu.id == current_id).first()
            if not parent_menu:
                break

            current_id = parent_menu.parent_id

    def _build_menu_tree(self, menus: List, parent_id: Optional[int] = None) -> List:
        """
        构建菜单树形结构

        Args:
            menus: 菜单列表
            parent_id: 父菜单ID

        Returns:
            菜单树列表
        """
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
