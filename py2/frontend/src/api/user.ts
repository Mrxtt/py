/**
 * 用户管理 API 服务
 */
import request from '@/utils/request';
import type {
  User,
  UserCreate,
  UserUpdate,
  UserUpdateStatus,
  UserAssignRoles,
  PageParams,
} from '@/types/rbac';
import type { ApiResponse, PageResponse } from '@/types/api';

/**
 * 创建用户
 */
export function createUser(data: UserCreate): Promise<ApiResponse<User>> {
  return request.post('/api/v1/users', data);
}

/**
 * 获取用户列表（分页）
 */
export function getUserList(params: PageParams): Promise<PageResponse<User>> {
  return request.get('/api/v1/users', { params });
}

/**
 * 获取用户详情
 */
export function getUserById(id: number): Promise<ApiResponse<User>> {
  return request.get(`/api/v1/users/${id}`);
}

/**
 * 更新用户
 */
export function updateUser(id: number, data: UserUpdate): Promise<ApiResponse<User>> {
  return request.put(`/api/v1/users/${id}`, data);
}

/**
 * 删除用户
 */
export function deleteUser(id: number): Promise<ApiResponse<null>> {
  return request.delete(`/api/v1/users/${id}`);
}

/**
 * 更新用户状态
 */
export function updateUserStatus(id: number, data: UserUpdateStatus): Promise<ApiResponse<User>> {
  return request.put(`/api/v1/users/${id}/status`, data);
}

/**
 * 获取用户角色
 */
export function getUserRoles(id: number): Promise<ApiResponse<any[]>> {
  return request.get(`/api/v1/users/${id}/roles`);
}

/**
 * 分配用户角色
 */
export function assignUserRoles(id: number, data: UserAssignRoles): Promise<ApiResponse<null>> {
  return request.post(`/api/v1/users/${id}/roles`, data);
}

export default {
  createUser,
  getUserList,
  getUserById,
  updateUser,
  deleteUser,
  updateUserStatus,
  getUserRoles,
  assignUserRoles,
};
