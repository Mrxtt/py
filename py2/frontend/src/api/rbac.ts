/**
 * RBAC API 服务
 */
import request from '../utils/request';
import type {
  Role,
  ApiResponse,
} from '../types';

/**
 * 获取当前用户权限
 */
export function getUserPermissions() {
  return request.get<ApiResponse<string[]>>('/api/v1/users/me/permissions');
}

/**
 * 获取当前用户角色
 */
export function getUserRoles() {
  return request.get<ApiResponse<Role[]>>('/api/v1/users/me/roles');
}

/**
 * 分配用户角色
 */
export function assignRoleToUser(userId: number, roleId: number) {
  return request.post<ApiResponse>(`/api/v1/users/${userId}/roles`, { role_id: roleId });
}

/**
 * 撤销用户角色
 */
export function revokeRoleFromUser(userId: number, roleId: number) {
  return request.delete<ApiResponse>(`/api/v1/users/${userId}/roles/${roleId}`);
}

/**
 * 分配角色权限
 */
export function assignPermissionToRole(roleId: number, permissionId: number) {
  return request.post<ApiResponse>(`/api/v1/roles/${roleId}/permissions`, { permission_id: permissionId });
}

/**
 * 撤销角色权限
 */
export function revokePermissionFromRole(roleId: number, permissionId: number) {
  return request.delete<ApiResponse>(`/api/v1/roles/${roleId}/permissions/${permissionId}`);
}

export default {
  getUserPermissions,
  getUserRoles,
  assignRoleToUser,
  revokeRoleFromUser,
  assignPermissionToRole,
  revokePermissionFromRole,
};
