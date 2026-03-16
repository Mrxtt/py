/**
 * 菜单相关类型定义
 */

/**
 * 菜单类型枚举
 */
export enum MenuType {
  DIRECTORY = 'directory',  // 目录
  MENU = 'menu',  // 菜单
  BUTTON = 'button',  // 按钮
}

/**
 * 菜单状态枚举
 */
export enum MenuStatus {
  ENABLED = 'enabled',
  DISABLED = 'disabled',
}

/**
 * 菜单接口
 */
export interface Menu {
  id: number;
  parent_id: number | null;
  name: string;
  icon: string | null;
  route: string | null;
  component: string | null;
  menu_type: MenuType;
  permission_code: string | null;
  sort_order: number;
  status: MenuStatus;
  created_at: string;
  updated_at: string;
}

/**
 * 菜单树节点接口
 */
export interface MenuTreeNode extends Menu {
  children: MenuTreeNode[];
}

/**
 * 菜单表单数据接口
 */
export interface MenuFormData {
  parent_id?: number | null;
  name: string;
  icon?: string;
  route?: string;
  component?: string;
  menu_type: MenuType;
  permission_code?: string;
  sort_order: number;
  status: MenuStatus;
}

/**
 * 菜单创建请求
 */
export interface MenuCreate extends MenuFormData {}

/**
 * 菜单更新请求
 */
export interface MenuUpdate extends Partial<MenuFormData> {}
