/**
 * 认证状态管理
 */
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { ElMessage } from 'element-plus';
import { login as loginApi, logout as logoutApi, getCurrentUser } from '@/api/auth';
import type { User, LoginRequest } from '@/types/rbac';
import type { LoginResponse } from '@/types/rbac';

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref<string | null>(localStorage.getItem('access_token'));
  const user = ref<User | null>(
    localStorage.getItem('user_info')
      ? JSON.parse(localStorage.getItem('user_info')!)
      : null
  );
  const rememberMe = ref<boolean>(false);

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value);

  // Actions
  /**
   * 用户登录
   */
  async function login(loginData: LoginRequest, remember: boolean = false) {
    try {
      const response = await loginApi(loginData);
      const { access_token, user: userData } = response.data;

      // 保存 token
      token.value = access_token;

      // 根据是否记住我选择存储方式
      if (remember) {
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('user_info', JSON.stringify(userData));
        rememberMe.value = true;
      } else {
        sessionStorage.setItem('access_token', access_token);
        sessionStorage.setItem('user_info', JSON.stringify(userData));
        rememberMe.value = false;
      }

      // 保存用户信息
      user.value = userData;

      ElMessage.success('登录成功');
      return true;
    } catch (error: any) {
      ElMessage.error(error.response?.data?.detail || '登录失败');
      return false;
    }
  }

  /**
   * 用户登出
   */
  async function logout() {
    try {
      await logoutApi();
    } catch (error) {
      console.error('登出失败:', error);
    } finally {
      // 清除本地存储
      localStorage.removeItem('access_token');
      localStorage.removeItem('user_info');
      sessionStorage.removeItem('access_token');
      sessionStorage.removeItem('user_info');

      // 清除状态
      token.value = null;
      user.value = null;
      rememberMe.value = false;

      ElMessage.success('登出成功');
    }
  }

  /**
   * 获取当前用户信息
   */
  async function fetchCurrentUser() {
    try {
      const response = await getCurrentUser();
      user.value = response.data;

      // 更新本地存储
      const storage = rememberMe.value ? localStorage : sessionStorage;
      storage.setItem('user_info', JSON.stringify(response.data));

      return user.value;
    } catch (error: any) {
      console.error('获取用户信息失败:', error);
      // 如果获取失败，清除登录状态
      await logout();
      return null;
    }
  }

  /**
   * 检查登录状态
   */
  function checkAuthStatus(): boolean {
    // 检查 token 是否存在
    const localToken = localStorage.getItem('access_token');
    const sessionToken = sessionStorage.getItem('access_token');

    if (localToken) {
      token.value = localToken;
      rememberMe.value = true;
    } else if (sessionToken) {
      token.value = sessionToken;
      rememberMe.value = false;
    } else {
      token.value = null;
      user.value = null;
      return false;
    }

    // 检查用户信息是否存在
    const storage = rememberMe.value ? localStorage : sessionStorage;
    const userInfo = storage.getItem('user_info');

    if (userInfo) {
      try {
        user.value = JSON.parse(userInfo);
        return true;
      } catch (error) {
        console.error('解析用户信息失败:', error);
        user.value = null;
        return false;
      }
    }

    return false;
  }

  /**
   * 更新用户信息
   */
  function updateUserInfo(userInfo: User) {
    user.value = userInfo;
    const storage = rememberMe.value ? localStorage : sessionStorage;
    storage.setItem('user_info', JSON.stringify(userInfo));
  }

  return {
    // State
    token,
    user,
    rememberMe,

    // Getters
    isAuthenticated,

    // Actions
    login,
    logout,
    fetchCurrentUser,
    checkAuthStatus,
    updateUserInfo,
  };
});
