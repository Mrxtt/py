<template>
  <div class="menu-tree">
    <el-tree
      ref="treeRef"
      :data="menuTreeData"
      :props="treeProps"
      :expand-on-click-node="false"
      :highlight-current="true"
      node-key="id"
      @node-click="handleNodeClick"
    >
      <template #default="{ node, data }">
        <span class="custom-tree-node">
          <span class="node-label">
            <el-icon v-if="data.icon" class="node-icon">
              <component :is="data.icon" />
            </el-icon>
            {{ node.label }}
          </span>
          <span class="node-actions">
            <el-button
              v-permission="['menu:create']"
              link
              type="primary"
              size="small"
              @click.stop="handleAdd(data)"
            >
              添加
            </el-button>
            <el-button
              v-permission="['menu:update']"
              link
              type="primary"
              size="small"
              @click.stop="handleEdit(data)"
            >
              编辑
            </el-button>
            <el-button
              v-permission="['menu:delete']"
              link
              type="danger"
              size="small"
              @click.stop="handleDelete(data)"
            >
              删除
            </el-button>
          </span>
        </span>
      </template>
    </el-tree>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElTree, ElMessage, ElMessageBox } from 'element-plus';
import { menuApi } from '../../api';
import type { MenuTreeNode } from '../../types';

// Props
interface Props {
  data?: MenuTreeNode[];
}

const props = withDefaults(defineProps<Props>(), {
  data: () => [],
});

// Emits
const emit = defineEmits<{
  add: [data: MenuTreeNode];
  edit: [data: MenuTreeNode];
  refresh: [];
}>();

// Refs
const treeRef = ref<InstanceType<typeof ElTree>>();
const menuTreeData = ref<MenuTreeNode[]>([]);

// Tree props
const treeProps = {
  children: 'children',
  label: 'name',
};

// 加载菜单树
async function loadMenuTree() {
  try {
    const res = await menuApi.getMenuTree();
    if (res.data.code === 200) {
      menuTreeData.value = res.data.data;
    }
  } catch (error) {
    console.error('加载菜单树失败:', error);
    ElMessage.error('加载菜单树失败');
  }
}

// 节点点击事件
function handleNodeClick(data: MenuTreeNode) {
  console.log('点击节点:', data);
}

// 添加子菜单
function handleAdd(data: MenuTreeNode) {
  emit('add', data);
}

// 编辑菜单
function handleEdit(data: MenuTreeNode) {
  emit('edit', data);
}

// 删除菜单
async function handleDelete(data: MenuTreeNode) {
  try {
    await ElMessageBox.confirm(
      `确定要删除菜单"${data.name}"吗？删除后将级联删除所有子菜单。`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );

    const res = await menuApi.deleteMenu(data.id);
    if (res.data.code === 200) {
      ElMessage.success('删除成功');
      await loadMenuTree();
      emit('refresh');
    } else {
      ElMessage.error(res.data.message || '删除失败');
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除菜单失败:', error);
      ElMessage.error('删除菜单失败');
    }
  }
}

// 刷新
async function refresh() {
  await loadMenuTree();
}

// 暴露方法
defineExpose({
  refresh,
});

// 初始化
onMounted(() => {
  if (props.data && props.data.length > 0) {
    menuTreeData.value = props.data;
  } else {
    loadMenuTree();
  }
});
</script>

<style scoped>
.menu-tree {
  padding: 16px;
}

.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-right: 8px;
  font-size: 14px;
}

.node-label {
  display: flex;
  align-items: center;
  gap: 4px;
}

.node-icon {
  font-size: 16px;
}

.node-actions {
  display: flex;
  gap: 4px;
}
</style>
