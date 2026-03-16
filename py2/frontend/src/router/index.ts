/**
 * 路由配置
 */
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
    meta: {
      title: '登录',
      requiresAuth: false,
    },
  },
  {
    path: '/',
    redirect: '/menu',
  },
  {
    path: '/menu',
    name: 'MenuManagement',
    component: () => import('../views/system/menu/index.vue'),
    meta: {
      title: '菜单管理',
      requiresAuth: true,
    },
  },
  {
    path: '/system/user',
    name: 'UserManagement',
    component: () => import('../views/system/user/index.vue'),
    meta: {
      title: '用户管理',
      requiresAuth: true,
    },
  },
  {
    path: '/system/role',
    name: 'RoleManagement',
    component: () => import('../views/system/role/index.vue'),
    meta: {
      title: '角色管理',
      requiresAuth: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 无限层菜单管理系统`;
  }

  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    // 检查登录状态
    const authStore = useAuthStore();
    if (!authStore.isAuthenticated) {
      // 未登录，跳转到登录页
      next('/login');
      return;
    }
  }

  // 如果已登录且访问登录页，重定向到首页
  if (to.path === '/login') {
    const authStore = useAuthStore();
    if (authStore.isAuthenticated) {
      next('/menu');
      return;
    }
  }

  next();
});

export default router;
