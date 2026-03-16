<template>
  <el-dialog
    title="分配权限"
    :model-value="visible"
    :close-on-click-modal="false"
    width="800px"
    @update:model-value="handleClose"
  >
    <div v-loading="loading">
      <el-tabs v-model="activeTab">
        <el-tab-pane
          v-for="group in permissionTree"
          :key="group.resource_type"
          :label="getResourceTypeLabel(group.resource_type)"
          :name="group.resource_type"
        >
          <el-checkbox-group v-model="selectedPermissionIds">
            <el-checkbox
              v-for="permission in group.permissions"
              :key="permission.id"
              :value="permission.id"
              :label="permission.permission_name"
            >
              {{ permission.permission_name }}（{{ permission.permission_code }}）
            </el-checkbox>
          </el-checkbox-group>
        </el-tab-pane>
      </el-tabs>
    </div>

    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" :loading="submitting" @click="handleSubmit">
        确定
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { getPermissionTree, getRolePermissions, updateRolePermissions } from '@/api/role';

interface Props {
  visible: boolean;
  roleId?: number;
}

interface Emits {
  (e: 'update:visible', value: boolean): void;
  (e: 'success'): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// 加载状态
const loading = ref(false);
const submitting = ref(false);

// 当前激活的标签页
const activeTab = ref('menu');

// 权限树
const permissionTree = ref<any[]>([]);

// 选中的权限ID
const selectedPermissionIds = ref<number[]>([]);

// 获取资源类型标签
function getResourceTypeLabel(resourceType: string) {
  const labelMap: Record<string, string> = {
    menu: '菜单权限',
    api: 'API权限',
    button: '按钮权限',
  };
  return labelMap[resourceType] || resourceType;
}

// 获取权限树
async function fetchPermissionTree() {
  loading.value = true;
  try {
    const response = await getPermissionTree();
    permissionTree.value = response.data;
    if (permissionTree.value.length > 0) {
      activeTab.value = permissionTree.value[0].resource_type;
    }
  } catch (error: any) {
    console.error('获取权限树失败:', error);
    ElMessage.error(error.response?.data?.detail || '获取权限树失败');
  } finally {
    loading.value = false;
  }
}

// 获取角色权限
async function fetchRolePermissions() {
  if (!props.roleId) return;

  try {
    const response = await getRolePermissions(props.roleId);
    selectedPermissionIds.value = response.data.map((perm: any) => perm.id);
  } catch (error: any) {
    console.error('获取角色权限失败:', error);
    ElMessage.error(error.response?.data?.detail || '获取角色权限失败');
  }
}

// 处理关闭
function handleClose() {
  emit('update:visible', false);
}

// 处理提交
async function handleSubmit() {
  if (!props.roleId) {
    ElMessage.error('角色ID不能为空');
    return;
  }

  submitting.value = true;
  try {
    await updateRolePermissions(props.roleId, {
      permission_ids: selectedPermissionIds.value,
    });
    ElMessage.success('权限分配成功');
    emit('success');
    handleClose();
  } catch (error: any) {
    console.error('权限分配失败:', error);
    ElMessage.error(error.response?.data?.detail || '权限分配失败');
  } finally {
    submitting.value = false;
  }
}

// 监听对话框显示状态
watch(
  () => props.visible,
  (newVisible) => {
    if (newVisible) {
      fetchPermissionTree();
      fetchRolePermissions();
    }
  }
);
</script>

<style scoped>
.el-checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 400px;
  overflow-y: auto;
}

.el-checkbox {
  margin-right: 0;
}
</style>
