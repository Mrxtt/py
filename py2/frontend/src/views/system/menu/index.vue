<template>
  <div class="menu-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>菜单管理</span>
          <el-button
            v-permission="['menu:create']"
            type="primary"
            @click="handleAddRoot"
          >
            添加根菜单
          </el-button>
        </div>
      </template>

      <div class="menu-container">
        <!-- 菜单树 -->
        <div class="menu-tree-section">
          <MenuTree
            ref="menuTreeRef"
            @add="handleAdd"
            @edit="handleEdit"
            @refresh="handleRefresh"
          />
        </div>
      </div>
    </el-card>

    <!-- 菜单表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      :close-on-click-modal="false"
      @close="handleDialogClose"
    >
      <MenuForm
        ref="menuFormRef"
        :data="currentMenuData"
        :parent-id="currentParentId"
        @submit="handleSubmit"
      />

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleDialogClose">取消</el-button>
          <el-button type="primary" @click="handleConfirmSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { MenuType, MenuStatus, MenuFormData, MenuTreeNode } from '../../../types';
import { menuApi } from '../../../api';
import MenuTree from '../../../components/menu/MenuTree.vue';
import MenuForm from '../../../components/menu/MenuForm.vue';

// Refs
const menuTreeRef = ref<InstanceType<typeof MenuTree>>();
const menuFormRef = ref<InstanceType<typeof MenuForm>>();

// 对话框状态
const dialogVisible = ref(false);
const dialogTitle = ref('添加菜单');
const dialogType = ref<'create' | 'update'>('create');

// 当前操作数据
const currentMenuData = ref<MenuFormData | null>(null);
const currentParentId = ref<number | null>(null);

// 添加根菜单
function handleAddRoot() {
  dialogTitle.value = '添加根菜单';
  dialogType.value = 'create';
  currentMenuData.value = null;
  currentParentId.value = null;
  dialogVisible.value = true;

  // 重置表单
  setTimeout(() => {
    menuFormRef.value?.resetForm();
  }, 100);
}

// 添加子菜单
function handleAdd(data: MenuTreeNode) {
  dialogTitle.value = `添加子菜单 - ${data.name}`;
  dialogType.value = 'create';
  currentMenuData.value = null;
  currentParentId.value = data.id;
  dialogVisible.value = true;

  // 重置表单
  setTimeout(() => {
    menuFormRef.value?.resetForm();
  }, 100);
}

// 编辑菜单
function handleEdit(data: MenuTreeNode) {
  dialogTitle.value = `编辑菜单 - ${data.name}`;
  dialogType.value = 'update';
  currentMenuData.value = {
    parent_id: data.parent_id,
    name: data.name,
    icon: data.icon,
    route: data.route,
    component: data.component,
    menu_type: data.menu_type,
    permission_code: data.permission_code,
    sort_order: data.sort_order,
    status: data.status,
  };
  currentParentId.value = null;
  dialogVisible.value = true;

  // 设置表单数据
  setTimeout(() => {
    menuFormRef.value?.setFormData(currentMenuData.value!);
  }, 100);
}

// 提交表单
async function handleSubmit(data: MenuFormData) {
  try {
    if (dialogType.value === 'create') {
      const res = await menuApi.createMenu(data);
      if (res.data.code === 200) {
        ElMessage.success('添加成功');
        dialogVisible.value = false;
        await menuTreeRef.value?.refresh();
      } else {
        ElMessage.error(res.data.message || '添加失败');
      }
    } else {
      const res = await menuApi.updateMenu(currentMenuData.value!.id!, data);
      if (res.data.code === 200) {
        ElMessage.success('更新成功');
        dialogVisible.value = false;
        await menuTreeRef.value?.refresh();
      } else {
        ElMessage.error(res.data.message || '更新失败');
      }
    }
  } catch (error) {
    console.error('提交失败:', error);
    ElMessage.error(dialogType.value === 'create' ? '添加失败' : '更新失败');
  }
}

// 确定提交
async function handleConfirmSubmit() {
  if (menuFormRef.value) {
    await menuFormRef.value.handleSubmit();
  }
}

// 关闭对话框
function handleDialogClose() {
  dialogVisible.value = false;
  currentMenuData.value = null;
  currentParentId.value = null;
}

// 刷新菜单树
function handleRefresh() {
  console.log('菜单树已刷新');
}
</script>

<style scoped>
.menu-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.menu-container {
  display: flex;
  gap: 20px;
}

.menu-tree-section {
  flex: 1;
  min-height: 500px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
