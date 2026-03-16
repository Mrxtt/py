<template>
  <div class="user-management">
    <el-card>
      <!-- 搜索栏 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.keyword"
            placeholder="用户名/邮箱/手机号/昵称"
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
            <el-option label="锁定" value="locked" />
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
          添加用户
        </el-button>
      </div>

      <!-- 用户列表 -->
      <el-table
        v-loading="loading"
        :data="userList"
        border
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="nickname" label="昵称" width="120" />
        <el-table-column prop="email" label="邮箱" width="180" />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_login_at" label="最后登录时间" width="180">
          <template #default="{ row }">
            {{ row.last_login_at ? formatDate(row.last_login_at) : '-' }}
          </template>
        </el-table-column>
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
            <el-button type="primary" size="small" @click="handleAssignRoles(row)">
              分配角色
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

    <!-- 用户表单对话框 -->
    <user-form-dialog
      v-model:visible="dialogVisible"
      :user="currentUser"
      @success="handleSearch"
    />

    <!-- 角色分配对话框 -->
    <role-select-dialog
      v-model:visible="roleDialogVisible"
      :user-id="currentUser?.id"
      @success="handleSearch"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Plus } from '@element-plus/icons-vue';
import { getUserList, deleteUser, updateUserStatus } from '@/api/user';
import type { User } from '@/types/rbac';
import UserFormDialog from '@/components/system/UserFormDialog.vue';
import RoleSelectDialog from '@/components/system/RoleSelectDialog.vue';

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

// 用户列表
const userList = ref<User[]>([]);

// 对话框显示状态
const dialogVisible = ref(false);
const roleDialogVisible = ref(false);

// 当前用户
const currentUser = ref<User | null>(null);

// 获取用户列表
async function fetchUserList() {
  loading.value = true;
  try {
    const response = await getUserList({
      page: pagination.page,
      page_size: pagination.page_size,
      keyword: searchForm.keyword || undefined,
      status: searchForm.status || undefined,
    });

    userList.value = response.data.items;
    pagination.total = response.data.total;
  } catch (error: any) {
    console.error('获取用户列表失败:', error);
    ElMessage.error(error.response?.data?.detail || '获取用户列表失败');
  } finally {
    loading.value = false;
  }
}

// 搜索
function handleSearch() {
  pagination.page = 1;
  fetchUserList();
}

// 重置
function handleReset() {
  searchForm.keyword = '';
  searchForm.status = '';
  handleSearch();
}

// 添加用户
function handleAdd() {
  currentUser.value = null;
  dialogVisible.value = true;
}

// 编辑用户
function handleEdit(user: User) {
  currentUser.value = user;
  dialogVisible.value = true;
}

// 更新用户状态
async function handleUpdateStatus(user: User, status: string) {
  try {
    await ElMessageBox.confirm(
      `确定要${status === 'active' ? '启用' : '禁用'}用户 "${user.username}" 吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );

    await updateUserStatus(user.id, { status: status as any });
    ElMessage.success('操作成功');
    fetchUserList();
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('更新状态失败:', error);
      ElMessage.error(error.response?.data?.detail || '操作失败');
    }
  }
}

// 分配角色
function handleAssignRoles(user: User) {
  currentUser.value = user;
  roleDialogVisible.value = true;
}

// 删除用户
async function handleDelete(user: User) {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${user.username}" 吗？此操作不可恢复！`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );

    await deleteUser(user.id);
    ElMessage.success('删除成功');
    fetchUserList();
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除用户失败:', error);
      ElMessage.error(error.response?.data?.detail || '删除失败');
    }
  }
}

// 获取状态类型
function getStatusType(status: string) {
  const statusMap: Record<string, any> = {
    active: 'success',
    inactive: 'info',
    locked: 'danger',
  };
  return statusMap[status] || 'info';
}

// 获取状态文本
function getStatusText(status: string) {
  const statusMap: Record<string, string> = {
    active: '启用',
    inactive: '禁用',
    locked: '锁定',
  };
  return statusMap[status] || status;
}

// 格式化日期
function formatDate(dateString: string) {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN');
}

// 组件挂载时获取用户列表
onMounted(() => {
  fetchUserList();
});
</script>

<style scoped>
.user-management {
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
