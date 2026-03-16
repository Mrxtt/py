<template>
  <div class="role-management">
    <el-card>
      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.keyword"
            placeholder="角色编码/角色名称/描述"
            clearable
            @clear="handleSearch"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-select
            v-model="searchForm.status"
            placeholder="请选择状态"
            clearable
            @clear="handleSearch"
          >
            <el-option label="启用" value="active" />
            <el-option label="禁用" value="inactive" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 操作栏 -->
      <div class="action-bar">
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          添加角色
        </el-button>
      </div>

      <!-- 角色列表 -->
      <el-table
        v-loading="loading"
        :data="roleList"
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="role_code" label="角色编码" width="150" />
        <el-table-column prop="role_name" label="角色名称" width="150" />
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sort_order" label="排序" width="80" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button
              v-if="row.status === 'active'"
              type="warning"
              size="small"
              @click="handleUpdateStatus(row, 'inactive')"
            >
              禁用
            </el-button>
            <el-button
              v-else
              type="success"
              size="small"
              @click="handleUpdateStatus(row, 'active')"
            >
              启用
            </el-button>
            <el-button type="primary" size="small" @click="handleAssignPermissions(row)">
              分配权限
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSearch"
        @current-change="handleSearch"
      />
    </el-card>

    <!-- 角色表单对话框 -->
    <role-form-dialog
      v-model:visible="dialogVisible"
      :role="currentRole"
      @success="handleSearch"
    />

    <!-- 权限分配对话框 -->
    <permission-select-dialog
      v-model:visible="permissionDialogVisible"
      :role-id="currentRole?.id"
      @success="handleSearch"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';
import { getRoleList, deleteRole, updateRoleStatus } from '@/api/role';
import type { Role } from '@/types/rbac';
import RoleFormDialog from '@/components/system/RoleFormDialog.vue';
import PermissionSelectDialog from '@/components/system/PermissionSelectDialog.vue';

// 加载状态
const loading = ref(false);

// 搜索表单
const searchForm = reactive({
  keyword: '',
  status: '',
});

// 分页
const pagination = reactive({
  page: 1,
  page_size: 10,
  total: 0,
});

// 角色列表
const roleList = ref<Role[]>([]);

// 对话框显示状态
const dialogVisible = ref(false);
const permissionDialogVisible = ref(false);

// 当前角色
const currentRole = ref<Role | null>(null);

// 获取角色列表
async function fetchRoleList() {
  loading.value = true;
  try {
    const response = await getRoleList({
      page: pagination.page,
      page_size: pagination.page_size,
      keyword: searchForm.keyword || undefined,
      status: searchForm.status || undefined,
    });

    roleList.value = response.data.items;
    pagination.total = response.data.total;
  } catch (error: any) {
    console.error('获取角色列表失败:', error);
    ElMessage.error(error.response?.data?.detail || '获取角色列表失败');
  } finally {
    loading.value = false;
  }
}

// 搜索
function handleSearch() {
  pagination.page = 1;
  fetchRoleList();
}

// 重置
function handleReset() {
  searchForm.keyword = '';
  searchForm.status = '';
  handleSearch();
}

// 添加角色
function handleAdd() {
  currentRole.value = null;
  dialogVisible.value = true;
}

// 编辑角色
function handleEdit(role: Role) {
  currentRole.value = role;
  dialogVisible.value = true;
}

// 更新角色状态
async function handleUpdateStatus(role: Role, status: string) {
  try {
    await ElMessageBox.confirm(
      `确定要${status === 'active' ? '启用' : '禁用'}角色 "${role.role_name}" 吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );

    await updateRoleStatus(role.id, { status: status as any });
    ElMessage.success('操作成功');
    fetchRoleList();
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('更新状态失败:', error);
      ElMessage.error(error.response?.data?.detail || '操作失败');
    }
  }
}

// 分配权限
function handleAssignPermissions(role: Role) {
  currentRole.value = role;
  permissionDialogVisible.value = true;
}

// 删除角色
async function handleDelete(role: Role) {
  try {
    await ElMessageBox.confirm(
      `确定要删除角色 "${role.role_name}" 吗？此操作不可恢复！`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );

    await deleteRole(role.id);
    ElMessage.success('删除成功');
    fetchRoleList();
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除角色失败:', error);
      ElMessage.error(error.response?.data?.detail || '删除失败');
    }
  }
}

// 获取状态类型
function getStatusType(status: string) {
  const statusMap: Record<string, any> = {
    active: 'success',
    inactive: 'info',
  };
  return statusMap[status] || 'info';
}

// 获取状态文本
function getStatusText(status: string) {
  const statusMap: Record<string, string> = {
    active: '启用',
    inactive: '禁用',
  };
  return statusMap[status] || status;
}

// 格式化日期
function formatDate(dateString: string) {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN');
}

// 组件挂载时获取角色列表
onMounted(() => {
  fetchRoleList();
});
</script>

<style scoped>
.role-management {
  padding: 20px;
}

.search-form {
  margin-bottom: 20px;
}

.action-bar {
  margin-bottom: 20px;
}

.el-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
