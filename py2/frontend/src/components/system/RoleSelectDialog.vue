<template>
  <el-dialog
    title="分配角色"
    :model-value="visible"
    :close-on-click-modal="false"
    width="600px"
    @update:model-value="handleClose"
  >
    <div v-loading="loading">
      <el-checkbox-group v-model="selectedRoleIds">
        <el-checkbox
          v-for="role in roleList"
          :key="role.id"
          :value="role.id"
          :label="role.role_name"
        >
          {{ role.role_name }}（{{ role.role_code }}）
        </el-checkbox>
      </el-checkbox-group>
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
import { getRoleList, getUserRoles, assignUserRoles } from '@/api/user';
import type { Role } from '@/types/rbac';

interface Props {
  visible: boolean;
  userId?: number;
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

// 角色列表
const roleList = ref<Role[]>([]);

// 选中的角色ID
const selectedRoleIds = ref<number[]>([]);

// 获取角色列表
async function fetchRoleList() {
  loading.value = true;
  try {
    const response = await getRoleList({ page: 1, page_size: 1000 });
    roleList.value = response.data.items;
  } catch (error: any) {
    console.error('获取角色列表失败:', error);
    ElMessage.error(error.response?.data?.detail || '获取角色列表失败');
  } finally {
    loading.value = false;
  }
}

// 获取用户角色
async function fetchUserRoles() {
  if (!props.userId) return;

  try {
    const response = await getUserRoles(props.userId);
    selectedRoleIds.value = response.data.map((role: any) => role.id);
  } catch (error: any) {
    console.error('获取用户角色失败:', error);
    ElMessage.error(error.response?.data?.detail || '获取用户角色失败');
  }
}

// 处理关闭
function handleClose() {
  emit('update:visible', false);
}

// 处理提交
async function handleSubmit() {
  if (!props.userId) {
    ElMessage.error('用户ID不能为空');
    return;
  }

  submitting.value = true;
  try {
    await assignUserRoles(props.userId, { role_ids: selectedRoleIds.value });
    ElMessage.success('角色分配成功');
    emit('success');
    handleClose();
  } catch (error: any) {
    console.error('角色分配失败:', error);
    ElMessage.error(error.response?.data?.detail || '角色分配失败');
  } finally {
    submitting.value = false;
  }
}

// 监听对话框显示状态
watch(
  () => props.visible,
  (newVisible) => {
    if (newVisible) {
      fetchRoleList();
      fetchUserRoles();
    }
  }
);
</script>

<style scoped>
.el-checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.el-checkbox {
  margin-right: 0;
}
</style>
