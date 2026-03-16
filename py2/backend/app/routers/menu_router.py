"""
菜单管理 API 路由
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..dependencies.auth import get_current_user, require_permission
from ..models import User
from ..models.enums import MenuStatus
from ..schemas.menu import MenuCreate, MenuUpdate, MenuResponse
from ..schemas.common import ApiResponse, PageResponse, PageData
from ..services import MenuService

# 创建路由器
router = APIRouter(prefix="/api/v1/menus", tags=["菜单管理"])


@router.post("", response_model=ApiResponse[MenuResponse], summary="创建菜单")
async def create_menu(
    menu_data: MenuCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("menu:create"))
):
    """
    创建新菜单

    - 需要权限: menu:create
    """
    try:
        menu_service = MenuService(db)
        menu = menu_service.create_menu(menu_data)
        return ApiResponse(code=200, message="创建成功", data=menu)
    except ValueError as e:
        return ApiResponse(code=400, message=str(e), data=None)


@router.get("", response_model=PageResponse[MenuResponse], summary="获取菜单列表")
async def get_menus(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回记录数"),
    status: Optional[MenuStatus] = Query(None, description="状态过滤"),
    menu_type: Optional[str] = Query(None, description="菜单类型过滤"),
    parent_id: Optional[int] = Query(None, description="父菜单ID过滤"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取菜单列表（支持分页和过滤）

    - 需要认证
    """
    menu_service = MenuService(db)
    menus, total = menu_service.get_menus(skip, limit, status, menu_type, parent_id)

    page_data = PageData(
        items=menus,
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        pages=(total + limit - 1) // limit
    )

    return PageResponse(code=200, message="查询成功", data=page_data)


@router.get("/tree", response_model=ApiResponse, summary="获取菜单树")
async def get_menu_tree(
    status: Optional[MenuStatus] = Query(None, description="状态过滤"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取菜单树结构

    - 需要认证
    """
    menu_service = MenuService(db)
    menu_tree = menu_service.get_menu_tree(status)

    return ApiResponse(code=200, message="查询成功", data=menu_tree)


@router.get("/{menu_id}", response_model=ApiResponse[MenuResponse], summary="获取菜单详情")
async def get_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    根据ID获取菜单详情

    - 需要认证
    """
    menu_service = MenuService(db)
    menu = menu_service.get_menu_by_id(menu_id)

    if not menu:
        return ApiResponse(code=404, message="菜单不存在", data=None)

    return ApiResponse(code=200, message="查询成功", data=menu)


@router.put("/{menu_id}", response_model=ApiResponse[MenuResponse], summary="更新菜单")
async def update_menu(
    menu_id: int,
    menu_data: MenuUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("menu:update"))
):
    """
    更新菜单信息

    - 需要权限: menu:update
    """
    try:
        menu_service = MenuService(db)
        menu = menu_service.update_menu(menu_id, menu_data)
        return ApiResponse(code=200, message="更新成功", data=menu)
    except ValueError as e:
        return ApiResponse(code=400, message=str(e), data=None)


@router.delete("/{menu_id}", response_model=ApiResponse, summary="删除菜单")
async def delete_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("menu:delete"))
):
    """
    删除菜单（级联删除子菜单）

    - 需要权限: menu:delete
    """
    menu_service = MenuService(db)
    success = menu_service.delete_menu(menu_id)

    if not success:
        return ApiResponse(code=404, message="菜单不存在", data=None)

    return ApiResponse(code=200, message="删除成功", data=None)


@router.get("/{menu_id}/children", response_model=ApiResponse[MenuResponse], summary="获取子菜单")
async def get_menu_children(
    menu_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取指定菜单的子菜单列表

    - 需要认证
    """
    menu_service = MenuService(db)
    children = menu_service.get_menu_children(menu_id)

    return ApiResponse(code=200, message="查询成功", data=children)
