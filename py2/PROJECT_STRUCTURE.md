# 项目结构总览

## 目录树

```
py1/
│
├── backend/                          # 后端项目目录
│   ├── app/                          # 应用主目录
│   │   ├── __init__.py
│   │   │
│   │   ├── core/                     # 核心配置模块
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # 应用配置（环境变量、JWT、CORS等）
│   │   │   ├── database.py          # 数据库配置（SQLAlchemy引擎、会话）
│   │   │   └── security.py          # 安全工具类（密码加密、JWT生成/验证）
│   │   │
│   │   ├── models/                   # 数据模型层
│   │   │   ├── __init__.py
│   │   │   ├── enums.py             # 枚举类型定义
│   │   │   ├── rbac.py              # RBAC模型（User、Role、Permission）
│   │   │   └── menu.py              # 菜单模型（Menu，支持自引用）
│   │   │
│   │   ├── schemas/                  # 数据验证层（Pydantic Schema）
│   │   │   ├── __init__.py
│   │   │   ├── common.py            # 通用响应模型（ApiResponse、PageResponse）
│   │   │   ├── rbac.py              # RBAC相关Schema（用户、角色、权限）
│   │   │   └── menu.py              # 菜单相关Schema（含XSS防护、路由验证）
│   │   │
│   │   ├── services/                 # 业务逻辑层
│   │   │   ├── __init__.py
│   │   │   ├── rbac_service.py      # RBAC核心服务（权限检查、角色分配）
│   │   │   └── menu_service.py      # 菜单管理服务（CRUD、循环引用检测）
│   │   │
│   │   ├── routers/                  # API路由层
│   │   │   ├── __init__.py
│   │   │   ├── auth_router.py       # 认证路由（登录、获取当前用户）
│   │   │   ├── menu_router.py       # 菜单管理路由（CRUD、树形查询）
│   │   │   └── rbac_router.py       # RBAC管理路由（用户权限、角色分配）
│   │   │
│   │   ├── dependencies/             # 依赖注入层
│   │   │   ├── __init__.py
│   │   │   └── auth.py              # 认证授权依赖（get_current_user、权限检查）
│   │   │
│   │   └── main.py                   # FastAPI主应用（路由注册、CORS配置）
│   │
│   ├── requirements.txt              # Python依赖清单
│   ├── .env.example                  # 环境变量示例文件
│   └── init_db.py                    # 数据库初始化脚本
│
├── frontend/                         # 前端项目目录
│   ├── src/
│   │   ├── api/                      # API服务层
│   │   │   ├── index.ts
│   │   │   ├── menu.ts              # 菜单API（CRUD、树形查询）
│   │   │   ├── auth.ts              # 认证API（登录、登出、获取用户信息）
│   │   │   └── rbac.ts              # RBAC API（权限查询、角色分配）
│   │   │
│   │   ├── types/                    # TypeScript类型定义
│   │   │   ├── index.ts
│   │   │   ├── menu.ts              # 菜单类型（Menu、MenuTreeNode、MenuFormData）
│   │   │   ├── rbac.ts              # RBAC类型（User、Role、Permission）
│   │   │   └── api.ts               # API响应类型（ApiResponse、PageResponse）
│   │   │
│   │   ├── stores/                   # Pinia状态管理
│   │   │   ├── index.ts
│   │   │   └── permission.ts        # 权限Store（权限检查、菜单树管理）
│   │   │
│   │   ├── directives/               # Vue自定义指令
│   │   │   ├── index.ts
│   │   │   └── permission.ts        # 权限指令（v-permission）
│   │   │
│   │   ├── components/               # Vue组件
│   │   │   └── menu/
│   │   │       ├── index.ts
│   │   │       ├── MenuTree.vue     # 菜单树组件（展示、展开/折叠、操作）
│   │   │       └── MenuForm.vue     # 菜单表单组件（添加、编辑）
│   │   │
│   │   ├── views/                    # 页面组件
│   │   │   └── system/
│   │   │       └── menu/
│   │   │           └── index.vue    # 菜单管理页面（整合树和表单）
│   │   │
│   │   ├── router/                   # 路由配置
│   │   │   └── index.ts             # Vue Router配置（路由守卫）
│   │   │
│   │   ├── utils/                    # 工具函数
│   │   │   └── request.ts           # Axios配置（拦截器、错误处理）
│   │   │
│   │   ├── App.vue                   # 根组件
│   │   └── main.ts                   # 应用入口（注册插件、挂载应用）
│   │
│   ├── package.json                  # Node.js依赖清单
│   ├── vite.config.ts                # Vite构建配置
│   ├── tsconfig.json                 # TypeScript配置
│   ├── tsconfig.node.json            # TypeScript Node环境配置
│   ├── index.html                    # HTML入口文件
│   └── .env.example                  # 环境变量示例文件
│
├── .codeartsdoer/                    # SDD文档目录
│   └── specs/
│       └── infinite-menu-dynamic-add/
│           ├── spec.md               # 需求规格说明（REQ-2.x）
│           ├── design.md             # 技术设计方案
│           └── tasks.md              # 编码任务清单
│
├── README.md                         # 项目说明文档
├── PROJECT_STRUCTURE.md              # 本文件
├── start.sh                          # Linux/Mac启动脚本
└── start.bat                         # Windows启动脚本
```

## 核心文件说明

### 后端核心文件

| 文件路径 | 说明 | 关键功能 |
|---------|------|---------|
| `backend/app/core/database.py` | 数据库配置 | SQLAlchemy引擎、会话管理 |
| `backend/app/core/security.py` | 安全工具 | 密码加密、JWT生成/验证 |
| `backend/app/models/menu.py` | 菜单模型 | 自引用关系、级联删除 |
| `backend/app/schemas/menu.py` | 菜单Schema | XSS防护、路由格式验证 |
| `backend/app/services/menu_service.py` | 菜单服务 | 循环引用检测、树形结构构建 |
| `backend/app/dependencies/auth.py` | 认证依赖 | JWT解析、权限检查工厂 |
| `backend/app/routers/menu_router.py` | 菜单路由 | RESTful API、权限保护 |

### 前端核心文件

| 文件路径 | 说明 | 关键功能 |
|---------|------|---------|
| `frontend/src/utils/request.ts` | Axios配置 | 请求/响应拦截、错误处理 |
| `frontend/src/api/menu.ts` | 菜单API | 封装菜单CRUD操作 |
| `frontend/src/stores/permission.ts` | 权限Store | 权限检查、菜单树管理 |
| `frontend/src/directives/permission.ts` | 权限指令 | v-permission指令实现 |
| `frontend/src/components/menu/MenuTree.vue` | 菜单树组件 | 树形展示、节点操作 |
| `frontend/src/components/menu/MenuForm.vue` | 菜单表单 | 表单验证、数据提交 |
| `frontend/src/views/system/menu/index.vue` | 菜单页面 | 组件整合、对话框管理 |

## 数据库表关系

```
users (用户表)
  └─> user_roles (关联表)
       └─> roles (角色表)
            └─> role_permissions (关联表)
                 └─> permissions (权限表)

menus (菜单表)
  └─> menus (自引用，parent_id)
```

## API 端点总览

### 菜单管理
- `POST /api/v1/menus` - 创建菜单
- `GET /api/v1/menus` - 获取菜单列表（分页）
- `GET /api/v1/menus/tree` - 获取菜单树
- `GET /api/v1/menus/{id}` - 获取菜单详情
- `PUT /api/v1/menus/{id}` - 更新菜单
- `DELETE /api/v1/menus/{id}` - 删除菜单
- `GET /api/v1/menus/{id}/children` - 获取子菜单

### 认证授权
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/auth/current` - 获取当前用户信息

### RBAC管理
- `GET /api/v1/users/me/permissions` - 获取用户权限
- `GET /api/v1/users/me/roles` - 获取用户角色
- `POST /api/v1/users/{id}/roles` - 分配用户角色
- `DELETE /api/v1/users/{id}/roles/{role_id}` - 撤销用户角色
- `POST /api/v1/roles/{id}/permissions` - 分配角色权限
- `DELETE /api/v1/roles/{id}/permissions/{permission_id}` - 撤销角色权限

## 权限编码规范

```
menu:create    - 创建菜单
menu:update    - 更新菜单
menu:delete    - 删除菜单
menu:view      - 查看菜单
admin          - 管理员角色
```

## 开发流程

1. **后端开发**
   - 修改 `models/` 定义数据模型
   - 修改 `schemas/` 定义数据验证
   - 修改 `services/` 实现业务逻辑
   - 修改 `routers/` 定义API端点

2. **前端开发**
   - 修改 `types/` 定义类型
   - 修改 `api/` 封装API调用
   - 修改 `stores/` 管理状态
   - 修改 `components/` 和 `views/` 实现UI

3. **测试**
   - 后端: 访问 `http://localhost:8000/docs` 测试API
   - 前端: 访问 `http://localhost:5173` 测试UI
