/**
 * RBAC 相关类型定义
 */

/**
 * 用户状态枚举
 */
export enum UserStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  LOCKED = 'locked',
}

/**
 * 角色状态枚举
 */
export enum RoleStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
}

/**
 * 权限状态枚举
 */
export enum PermissionStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
}

/**
 * 用户接口
 */
export interface User {
  id: number;
  username: string;
  email: string | null;
  phone: string | null;
  nickname: string | null;
  avatar: string | null;
  status: UserStatus;
  last_login_at: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * 角色接口
 */
export interface Role {
  id: number;
  role_code: string;
  role_name: string;
  description: string | null;
  status: RoleStatus;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

/**
 * 权限接口
 */
export interface Permission {
  id: number;
  permission_code: string;
  permission_name: string;
  resource_type: string;
  resource_id: number | null;
  description: string | null;
  status: PermissionStatus;
  created_at: string;
  updated_at: string;
}

/**
 * 登录请求
 */
export interface LoginRequest {
  username: string;
  password: string;
}

/**
 * 登录响应
 */
export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// ==================== 用户管理相关类型 ====================

/**
 * 用户创建请求
 */
export interface UserCreate {
  username: string;
  password: string;
  email?: string;
  phone?: string;
  nickname?: string;
  avatar?: string;
  status?: UserStatus;
}

/**
 * 用户更新请求
 */
export interface UserUpdate {
  email?: string;
  phone?: string;
  nickname?: string;
  avatar?: string;
  status?: UserStatus;
}

/**
 * 用户状态更新请求
 */
export interface UserUpdateStatus {
  status: UserStatus;
}

/**
 * 用户角色分配请求
 */
export interface UserAssignRoles {
  role_ids: number[];
}

// ==================== 角色管理相关类型 ====================

/**
 * 角色创建请求
 */
export interface RoleCreate {
  role_code: string;
  role_name: string;
  description?: string;
  status?: RoleStatus;
  sort_order?: number;
}

/**
 * 角色更新请求
 */
export interface RoleUpdate {
  role_name?: string;
  description?: string;
  status?: RoleStatus;
  sort_order?: number;
}

/**
 * 角色状态更新请求
 */
export interface RoleUpdateStatus {
  status: RoleStatus;
}

/**
 * 角色权限更新请求
 */
export interface RoleUpdatePermissions {
  permission_ids: number[];
}

// ==================== 分页参数 ====================

/**
 * 分页查询参数
 */
export interface PageParams {
  page?: number;
  page_size?: number;
  keyword?: string;
  status?: string;
}
