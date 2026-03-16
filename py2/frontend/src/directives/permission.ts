/**
 * 权限指令
 */
import type { Directive, DirectiveBinding } from 'vue';
import { usePermissionStore } from '../stores/permission';

export const permission: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const { value } = binding;
    const permissionStore = usePermissionStore();

    if (value && value instanceof Array && value.length > 0) {
      const requiredPermissions = value as string[];

      // 检查是否拥有任意一个权限
      const hasPermission = permissionStore.hasAnyPermission(requiredPermissions);

      if (!hasPermission) {
        // 移除元素
        el.parentNode?.removeChild(el);
      }
    } else if (value && typeof value === 'string') {
      const requiredPermission = value as string;

      // 检查是否拥有权限
      const hasPermission = permissionStore.hasPermission(requiredPermission);

      if (!hasPermission) {
        // 移除元素
        el.parentNode?.removeChild(el);
      }
    } else {
      throw new Error('need permissions! Like v-permission="[\'user:add\',\'user:edit\']" or v-permission="\'user:add\'"');
    }
  },
};

export default permission;
