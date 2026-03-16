<template>
  <el-dialog
    :title="isEdit ? '编辑角色' : '添加角色'"
    :model-value="visible"
    :close-on-click-modal="false"
    width="600px"
    @update:model-value="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="100px"
    >
      <el-form-item label="角色编码" prop="role_code">
        <el-input
          v-model="formData.role_code"
          placeholder="请输入角色编码"
          :disabled="isEdit"
        />
      </el-form-item>

      <el-form-item label="角色名称" prop="role_name">
        <el-input
          v-model="formData.role_name"
          placeholder="请输入角色名称"
        />
      </el-form-item>

      <el-form-item label="描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入角色描述"
        />
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-select v-model="formData.status" placeholder="请选择状态">
          <el-option label="启用" value="active" />
          <el-option label="禁用" value="inactive" />
        </el-select>
      </el-form-item>

      <el-form-item label="排序" prop="sort_order">
        <el-input-number
          v-model="formData.sort_order"
          :min="0"
          :max="9999"
          placeholder="请输入排序"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" :loading="loading" @click="handleSubmit">
        确定
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { reactive, ref, watch, computed } from 'vue';
import { ElMessage, type FormInstance, type FormRules } from 'element-plus';
import { createRole, updateRole } from '@/api/role';
import type { Role, RoleCreate, RoleUpdate } from '@/types/rbac';

interface Props {
  visible: boolean;
  role?: Role | null;
}

interface Emits {
  (e: 'update:visible', value: boolean): void;
  (e: 'success'): void;
}

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

// 表单引用
const formRef = ref<FormInstance>();

// 加载状态
const loading = ref(false);

// 是否为编辑模式
const isEdit = computed(() => !!props.role);

// 表单数据
const formData = reactive<RoleCreate>({
  role_code: '',
  role_name: '',
  description: '',
  status: 'active',
  sort_order: 0,
});

// 表单验证规则
const formRules: FormRules = {
  role_code: [
    { required: true, message: '请输入角色编码', trigger: 'blur' },
    { min: 2, max: 50, message: '角色编码长度在 2 到 50 个字符', trigger: 'blur' },
    {
      pattern: /^[a-zA-Z0-9_-]+$/,
      message: '角色编码只能包含字母、数字、下划线和连字符',
      trigger: 'blur',
    },
  ],
  role_name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' },
    { min: 2, max: 50, message: '角色名称长度在 2 到 50 个字符', trigger: 'blur' },
  ],
};

// 监听角色数据变化
watch(
  () => props.role,
  (newRole) => {
    if (newRole) {
      // 编辑模式，填充表单数据
      formData.role_code = newRole.role_code;
      formData.role_name = newRole.role_name;
      formData.description = newRole.description || '';
      formData.status = newRole.status;
      formData.sort_order = newRole.sort_order;
    } else {
      // 新增模式，重置表单
      formData.role_code = '';
      formData.role_name = '';
      formData.description = '';
      formData.status = 'active';
      formData.sort_order = 0;
    }
  },
  { immediate: true }
);

// 处理关闭
function handleClose() {
  emit('update:visible', false);
  formRef.value?.clearValidate();
}

// 处理提交
async function handleSubmit() {
  if (!formRef.value) return;

  try {
    // 验证表单
    await formRef.value.validate();

    loading.value = true;

    if (isEdit.value && props.role) {
      // 更新角色
      const updateData: RoleUpdate = {
        role_name: formData.role_name,
        description: formData.description,
        status: formData.status,
        sort_order: formData.sort_order,
      };
      await updateRole(props.role.id, updateData);
      ElMessage.success('更新成功');
    } else {
      // 创建角色
      await createRole(formData);
      ElMessage.success('创建成功');
    }

    emit('success');
    handleClose();
  } catch (error: any) {
    console.error('提交失败:', error);
    ElMessage.error(error.response?.data?.detail || '操作失败');
  } finally {
    loading.value = false;
  }
}
</script>
