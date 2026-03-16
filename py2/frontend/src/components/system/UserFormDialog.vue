<template>
  <el-dialog
    :title="isEdit ? '编辑用户' : '添加用户'"
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
      <el-form-item label="用户名" prop="username">
        <el-input
          v-model="formData.username"
          placeholder="请输入用户名"
          :disabled="isEdit"
        />
      </el-form-item>

      <el-form-item v-if="!isEdit" label="密码" prop="password">
        <el-input
          v-model="formData.password"
          type="password"
          placeholder="请输入密码"
          show-password
        />
      </el-form-item>

      <el-form-item label="邮箱" prop="email">
        <el-input
          v-model="formData.email"
          placeholder="请输入邮箱"
        />
      </el-form-item>

      <el-form-item label="手机号" prop="phone">
        <el-input
          v-model="formData.phone"
          placeholder="请输入手机号"
        />
      </el-form-item>

      <el-form-item label="昵称" prop="nickname">
        <el-input
          v-model="formData.nickname"
          placeholder="请输入昵称"
        />
      </el-form-item>

      <el-form-item label="状态" prop="status">
        <el-select v-model="formData.status" placeholder="请选择状态">
          <el-option label="启用" value="active" />
          <el-option label="禁用" value="inactive" />
          <el-option label="锁定" value="locked" />
        </el-select>
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
import { reactive, ref, watch } from 'vue';
import { ElMessage, type FormInstance, type FormRules } from 'element-plus';
import { createUser, updateUser } from '@/api/user';
import type { User, UserCreate, UserUpdate } from '@/types/rbac';

interface Props {
  visible: boolean;
  user?: User | null;
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
const isEdit = computed(() => !!props.user);

// 表单数据
const formData = reactive<UserCreate>({
  username: '',
  password: '',
  email: '',
  phone: '',
  nickname: '',
  avatar: '',
  status: 'active',
});

// 表单验证规则
const formRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在 3 到 50 个字符', trigger: 'blur' },
    {
      pattern: /^[a-zA-Z0-9_]+$/,
      message: '用户名只能包含字母、数字和下划线',
      trigger: 'blur',
    },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' },
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' },
  ],
  phone: [
    {
      pattern: /^1[3-9]\d{9}$/,
      message: '请输入正确的手机号',
      trigger: 'blur',
    },
  ],
};

// 监听用户数据变化
watch(
  () => props.user,
  (newUser) => {
    if (newUser) {
      // 编辑模式，填充表单数据
      formData.username = newUser.username;
      formData.email = newUser.email || '';
      formData.phone = newUser.phone || '';
      formData.nickname = newUser.nickname || '';
      formData.avatar = newUser.avatar || '';
      formData.status = newUser.status;
    } else {
      // 新增模式，重置表单
      formData.username = '';
      formData.password = '';
      formData.email = '';
      formData.phone = '';
      formData.nickname = '';
      formData.avatar = '';
      formData.status = 'active';
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

    if (isEdit.value && props.user) {
      // 更新用户
      const updateData: UserUpdate = {
        email: formData.email,
        phone: formData.phone,
        nickname: formData.nickname,
        avatar: formData.avatar,
        status: formData.status,
      };
      await updateUser(props.user.id, updateData);
      ElMessage.success('更新成功');
    } else {
      // 创建用户
      await createUser(formData);
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
