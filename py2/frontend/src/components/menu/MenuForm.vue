<template>
  <el-form
    ref="formRef"
    :model="formData"
    :rules="formRules"
    label-width="120px"
    @submit.prevent="handleSubmit"
  >
    <el-form-item label="父菜单" prop="parent_id">
      <el-tree-select
        v-model="formData.parent_id"
        :data="menuTreeOptions"
        :props="treeSelectProps"
        :render-after-expand="false"
        placeholder="请选择父菜单（不选则为根菜单）"
        clearable
        check-strictly
      />
    </el-form-item>

    <el-form-item label="菜单名称" prop="name">
      <el-input v-model="formData.name" placeholder="请输入菜单名称" />
    </el-form-item>

    <el-form-item label="菜单类型" prop="menu_type">
      <el-select v-model="formData.menu_type" placeholder="请选择菜单类型">
        <el-option label="目录" :value="MenuType.DIRECTORY" />
        <el-option label="菜单" :value="MenuType.MENU" />
        <el-option label="按钮" :value="MenuType.BUTTON" />
      </el-select>
    </el-form-item>

    <el-form-item label="菜单图标" prop="icon">
      <el-input v-model="formData.icon" placeholder="请输入菜单图标（Element Plus 图标名）" />
    </el-form-item>

    <el-form-item label="路由路径" prop="route">
      <el-input v-model="formData.route" placeholder="请输入路由路径，如 /system/user" />
    </el-form-item>

    <el-form-item label="组件路径" prop="component">
      <el-input v-model="formData.component" placeholder="请输入组件路径，如 /system/user/index" />
    </el-form-item>

    <el-form-item label="权限编码" prop="permission_code">
      <el-input v-model="formData.permission_code" placeholder="请输入权限编码，如 system:user:view" />
    </el-form-item>

    <el-form-item label="排序" prop="sort_order">
      <el-input-number v-model="formData.sort_order" :min="0" :max="9999" />
    </el-form-item>

    <el-form-item label="状态" prop="status">
      <el-radio-group v-model="formData.status">
        <el-radio :label="MenuStatus.ENABLED">启用</el-radio>
        <el-radio :label="MenuStatus.DISABLED">禁用</el-radio>
      </el-radio-group>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';
import { MenuType, MenuStatus, MenuFormData, MenuTreeNode } from '../../types';
import { menuApi } from '../../api';

// Props
interface Props {
  data?: MenuFormData | null;
  parentId?: number | null;
}

const props = withDefaults(defineProps<Props>(), {
  data: null,
  parentId: null,
});

// Emits
const emit = defineEmits<{
  submit: [data: MenuFormData];
}>();

// Refs
const formRef = ref<FormInstance>();
const menuTreeOptions = ref<MenuTreeNode[]>([]);

// 表单数据
const formData = reactive<MenuFormData>({
  parent_id: null,
  name: '',
  icon: '',
  route: '',
  component: '',
  menu_type: MenuType.MENU,
  permission_code: '',
  sort_order: 0,
  status: MenuStatus.ENABLED,
});

// 表单验证规则
const formRules: FormRules = {
  name: [
    { required: true, message: '请输入菜单名称', trigger: 'blur' },
    { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' },
  ],
  menu_type: [
    { required: true, message: '请选择菜单类型', trigger: 'change' },
  ],
  route: [
    { pattern: /^\/[\w\-/]*$/, message: '路由路径格式不正确', trigger: 'blur' },
  ],
  sort_order: [
    { required: true, message: '请输入排序值', trigger: 'blur' },
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' },
  ],
};

// Tree Select props
const treeSelectProps = {
  value: 'id',
  label: 'name',
  children: 'children',
};

// 加载菜单树选项
async function loadMenuTreeOptions() {
  try {
    const res = await menuApi.getMenuTree();
    if (res.data.code === 200) {
      menuTreeOptions.value = res.data.data;
    }
  } catch (error) {
    console.error('加载菜单树失败:', error);
  }
}

// 提交表单
async function handleSubmit() {
  if (!formRef.value) return;

  try {
    await formRef.value.validate();
    emit('submit', { ...formData });
  } catch (error) {
    console.error('表单验证失败:', error);
  }
}

// 验证表单
async function validate() {
  if (!formRef.value) return false;
  return await formRef.value.validate();
}

// 重置表单
function resetForm() {
  if (!formRef.value) return;
  formRef.value.resetFields();
  formData.parent_id = props.parentId || null;
  formData.name = '';
  formData.icon = '';
  formData.route = '';
  formData.component = '';
  formData.menu_type = MenuType.MENU;
  formData.permission_code = '';
  formData.sort_order = 0;
  formData.status = MenuStatus.ENABLED;
}

// 设置表单数据
function setFormData(data: MenuFormData) {
  Object.assign(formData, data);
}

// 暴露方法
defineExpose({
  validate,
  resetForm,
  setFormData,
  handleSubmit,
});

// 初始化
onMounted(() => {
  loadMenuTreeOptions();

  if (props.data) {
    setFormData(props.data);
  } else if (props.parentId) {
    formData.parent_id = props.parentId;
  }
});
</script>

<style scoped>
/* 可以添加自定义样式 */
</style>
