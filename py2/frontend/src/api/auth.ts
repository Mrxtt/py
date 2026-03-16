/**
 * 认证 API 服务
 */
import request from '../utils/request';
import type {
  LoginRequest,
  LoginResponse,
  User,
  ApiResponse,
} from '../types';

/**
 * 用户登录
 */
export function login(data: LoginRequest) {
  return request.post<ApiResponse<LoginResponse>>('/api/v1/auth/login', data);
}

/**
 * 获取当前用户信息
 */
export function getCurrentUser() {
  return request.get<ApiResponse<User>>('/api/v1/auth/current');
}

/**
 * 登出
 */
export function logout() {
  // 清除本地存储的 token 和用户信息
  localStorage.removeItem('access_token');
  localStorage.removeItem('user_info');
  return Promise.resolve();
}

export default {
  login,
  getCurrentUser,
  logout,
};
