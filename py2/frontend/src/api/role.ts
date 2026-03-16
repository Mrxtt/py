/**
 * 角色管理 API 服务
 */
import request from '@/utils/request';
import type {
  Role,
  RoleCreate,
  RoleUpdate,
  RoleUpdateStatus,
  RoleUpdatePermissions,
  PageParams,
} from '@/types/rbac';
import type { ApiResponse, PageResponse } from '@/types/api';

/**
 * 创建角色
 */
export function createRole(data: RoleCreate): Promise<ApiResponse<Role>> {
  return request.post('/api/v1/roles', data);
}

/**
 * 获取角色列表（分页）
 */
export function getRoleList(params: PageParams): Promise<PageResponse<Role>> {
  return request.get('/api/v1/roles', { params });
}

/**
 * 获取角色详情
 */
export function getRoleById(id: number): Promise<ApiResponse<Role>> {
  return request.get(`/api/v1/roles/${id}`);
}

/**
 * 更新角色
 */
export function updateRole(id: number, data: RoleUpdate): Promise<ApiResponse<Role>> {
  return request.put(`/api/v1/roles/${id}`, data);
}

/**
 * 删除角色
 */
export function deleteRole(id: number): Promise<ApiResponse<null>> {
  return request.delete(`/api/v1/roles/${id}`);
}

/**
 * 更新角色状态
 */
export function updateRoleStatus(id: number, data: RoleUpdateStatus): Promise<ApiResponse<Role>> {
  return request.put(`/api/v1/roles/${id}/status`, data);
}

/**
 * 获取角色权限
 */
export function getRolePermissions(id: number): Promise<ApiResponse<any[]>> {
  return request.get(`/api/v1/roles/${id}/permissions`);
}

/**
 * 更新角色权限
 */
export function updateRolePermissions(id: number, data: RoleUpdatePermissions): Promise<ApiResponse<null>> {
  return request.put(`/api/v1/roles/${id}/permissions`, data);
}

export default {
  createRole,
  getRoleList,
  getRoleById,
  updateRole,
  deleteRole,
  updateRoleStatus,
  getRolePermissions,
  updateRolePermissions,
};
