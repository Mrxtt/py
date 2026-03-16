/**
 * 权限管理 Store
 */
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { MenuTreeNode } from '../types';
import { rbacApi, menuApi } from '../api';

export const usePermissionStore = defineStore('permission', () => {
  // 状态
  const permissions = ref<string[]>([]);
  const roles = ref<string[]>([]);
  const menuTree = ref<MenuTreeNode[]>([]);
  const loaded = ref(false);

  // 计算属性
  const hasPermissions = computed(() => permissions.value.length > 0);
  const hasRoles = computed(() => roles.value.length > 0);
  const hasMenuTree = computed(() => menuTree.value.length > 0);

  /**
   * 加载用户权限和角色
   */
  async function loadPermissions() {
    try {
      const [permRes, roleRes] = await Promise.all([
        rbacApi.getUserPermissions(),
        rbacApi.getUserRoles(),
      ]);

      if (permRes.data.code === 200) {
        permissions.value = permRes.data.data;
      }

      if (roleRes.data.code === 200) {
        roles.value = roleRes.data.data.map((role) => role.role_code);
      }

      loaded.value = true;
    } catch (error) {
      console.error('加载权限失败:', error);
    }
  }

  /**
   * 加载用户菜单树
   */
  async function loadMenuTree() {
    try {
      const res = await menuApi.getMenuTree();
      if (res.data.code === 200) {
        menuTree.value = res.data.data;
      }
    } catch (error) {
      console.error('加载菜单树失败:', error);
    }
  }

  /**
   * 检查是否拥有指定权限
   */
  function hasPermission(permission: string): boolean {
    return permissions.value.includes(permission);
  }

  /**
   * 检查是否拥有任意权限
   */
  function hasAnyPermission(permList: string[]): boolean {
    return permList.some((perm) => permissions.value.includes(perm));
  }

  /**
   * 检查是否拥有所有权限
   */
  function hasAllPermissions(permList: string[]): boolean {
    return permList.every((perm) => permissions.value.includes(perm));
  }

  /**
   * 检查是否拥有指定角色
   */
  function hasRole(role: string): boolean {
    return roles.value.includes(role);
  }

  /**
   * 检查是否拥有任意角色
   */
  function hasAnyRole(roleList: string[]): boolean {
    return roleList.some((role) => roles.value.includes(role));
  }

  /**
   * 清空权限数据
   */
  function clearPermissions() {
    permissions.value = [];
    roles.value = [];
    menuTree.value = [];
    loaded.value = false;
  }

  return {
    // 状态
    permissions,
    roles,
    menuTree,
    loaded,

    // 计算属性
    hasPermissions,
    hasRoles,
    hasMenuTree,

    // 方法
    loadPermissions,
    loadMenuTree,
    hasPermission,
    hasAnyPermission,
    hasAllPermissions,
    hasRole,
    hasAnyRole,
    clearPermissions,
  };
});
