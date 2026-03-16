/**
 * 菜单 API 服务
 */
import request from '../utils/request';
import type {
  Menu,
  MenuTreeNode,
  MenuCreate,
  MenuUpdate,
  ApiResponse,
  PageResponse,
  MenuStatus,
} from '../types';

/**
 * 创建菜单
 */
export function createMenu(data: MenuCreate) {
  return request.post<ApiResponse<Menu>>('/api/v1/menus', data);
}

/**
 * 获取菜单列表
 */
export function getMenuList(params?: {
  skip?: number;
  limit?: number;
  status?: MenuStatus;
  menu_type?: string;
  parent_id?: number;
}) {
  return request.get<PageResponse<Menu>>('/api/v1/menus', { params });
}

/**
 * 获取菜单树
 */
export function getMenuTree(params?: {
  status?: MenuStatus;
}) {
  return request.get<ApiResponse<MenuTreeNode[]>>('/api/v1/menus/tree', { params });
}

/**
 * 根据ID获取菜单详情
 */
export function getMenuById(id: number) {
  return request.get<ApiResponse<Menu>>(`/api/v1/menus/${id}`);
}

/**
 * 更新菜单
 */
export function updateMenu(id: number, data: MenuUpdate) {
  return request.put<ApiResponse<Menu>>(`/api/v1/menus/${id}`, data);
}

/**
 * 删除菜单
 */
export function deleteMenu(id: number) {
  return request.delete<ApiResponse>(`/api/v1/menus/${id}`);
}

/**
 * 获取子菜单
 */
export function getMenuChildren(id: number) {
  return request.get<ApiResponse<Menu[]>>(`/api/v1/menus/${id}/children`);
}

export default {
  createMenu,
  getMenuList,
  getMenuTree,
  getMenuById,
  updateMenu,
  deleteMenu,
  getMenuChildren,
};
