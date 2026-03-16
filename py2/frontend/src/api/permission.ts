/**
 * 权限查询 API 服务
 */
import request from '@/utils/request';
import type { Permission } from '@/types/rbac';
import type { ApiResponse } from '@/types/api';

/**
 * 获取所有权限
 */
export function getPermissionList(): Promise<ApiResponse<Permission[]>> {
  return request.get('/api/v1/permissions');
}

/**
 * 获取权限树
 */
export function getPermissionTree(): Promise<ApiResponse<any[]>> {
  return request.get('/api/v1/permissions/tree');
}

export default {
  getPermissionList,
  getPermissionTree,
};
