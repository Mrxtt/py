# 无限层菜单动态添加系统

基于 Python3 FastAPI 后端 + Vue3 + TypeScript + ElementPlus 前端的无限层菜单动态添加管理系统。

## 项目结构

```
py1/
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── core/           # 核心配置
│   │   │   ├── database.py # 数据库配置
│   │   │   ├── config.py   # 应用配置
│   │   │   └── security.py # 安全工具类
│   │   ├── models/         # 数据模型
│   │   │   ├── enums.py    # 枚举类型
│   │   │   ├── rbac.py     # RBAC模型
│   │   │   └── menu.py     # 菜单模型
│   │   ├── schemas/        # Pydantic Schema
│   │   │   ├── common.py   # 通用响应模型
│   │   │   ├── rbac.py     # RBAC Schema
│   │   │   └── menu.py     # 菜单 Schema
│   │   ├── services/       # 业务逻辑层
│   │   │   ├── rbac_service.py  # RBAC服务
│   │   │   └── menu_service.py  # 菜单服务
│   │   ├── routers/        # API路由
│   │   │   ├── auth_router.py   # 认证路由
│   │   │   ├── menu_router.py   # 菜单路由
│   │   │   └── rbac_router.py   # RBAC路由
│   │   ├── dependencies/   # 依赖注入
│   │   │   └── auth.py     # 认证授权依赖
│   │   └── main.py         # FastAPI主应用
│   ├── requirements.txt    # Python依赖
│   ├── .env.example        # 环境变量示例
│   └── init_db.py          # 数据库初始化脚本
│
├── frontend/               # 前端项目
│   ├── src/
│   │   ├── api/           # API服务层
│   │   │   ├── menu.ts    # 菜单API
│   │   │   ├── auth.ts    # 认证API
│   │   │   └── rbac.ts    # RBAC API
│   │   ├── types/         # TypeScript类型定义
│   │   │   ├── menu.ts    # 菜单类型
│   │   │   ├── rbac.ts    # RBAC类型
│   │   │   └── api.ts     # API响应类型
│   │   ├── stores/        # Pinia状态管理
│   │   │   └── permission.ts  # 权限Store
│   │   ├── directives/    # Vue指令
│   │   │   └── permission.ts  # 权限指令
│   │   ├── components/    # 组件
│   │   │   └── menu/      # 菜单组件
│   │   │       ├── MenuTree.vue   # 菜单树组件
│   │   │       └── MenuForm.vue   # 菜单表单组件
│   │   ├── views/         # 页面
│   │   │   └── system/
│   │   │       └── menu/
│   │   │           └── index.vue  # 菜单管理页面
│   │   ├── router/        # 路由配置
│   │   ├── utils/         # 工具函数
│   │   │   └── request.ts # Axios配置
│   │   ├── App.vue        # 根组件
│   │   └── main.ts        # 入口文件
│   ├── package.json       # Node依赖
│   ├── vite.config.ts     # Vite配置
│   ├── tsconfig.json      # TypeScript配置
│   └── .env.example       # 环境变量示例
│
└── .codeartsdoer/         # SDD文档目录
    └── specs/
        └── infinite-menu-dynamic-add/
            ├── spec.md     # 需求规格说明
            ├── design.md   # 技术设计方案
            └── tasks.md    # 编码任务清单
```

## 技术栈

### 后端
- **框架**: FastAPI 0.104.1
- **数据库**: MySQL + SQLAlchemy 2.0.23
- **认证**: JWT (python-jose)
- **密码加密**: bcrypt (passlib)
- **数据验证**: Pydantic 2.5.0

### 前端
- **框架**: Vue 3.3.8
- **语言**: TypeScript 5.3.2
- **构建工具**: Vite 5.0.5
- **UI组件库**: Element Plus 2.4.4
- **状态管理**: Pinia 2.1.7
- **路由**: Vue Router 4.2.5- **HTTP客户端**: Axios 1.6.2

## 核心功能

### 1. 无限层菜单管理
- 支持无限层级菜单结构
- 动态添加、编辑、删除菜单
- 菜单树形展示
- 循环引用检测
- 同级菜单名称唯一性验证

### 2. RBAC权限管理
- 用户-角色-权限三级权限模型
- 灵活的权限配置
- 基于角色的访问控制
- 权限指令（v-permission）
- 菜单权限绑定

### 3. 认证授权
- JWT Token 认证
- 密码 bcrypt 加密
- 登录状态管理
- 自动刷新机制

## 快速开始

### 后端启动

1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

2. 配置数据库
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库连接信息
```

3. 初始化数据库
```bash
python init_db.py
```

4. 启动服务
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. 访问 API 文档
```
http://localhost:8000/docs
```

### 前端启动

1. 安装依赖
```bash
cd frontend
npm install
```

2. 配置环境变量
```bash
cp .env.example .env
```

3. 启动开发服务器
```bash
npm run dev
```

4. 访问应用
```
http://localhost:5173
```

## 数据库表结构

### 用户表 (users)
- id: 主键
- username: 用户名
- password: 密码（加密）
- email: 邮箱
- phone: 手机号
- nickname: 昵称
- avatar: 头像
- status: 状态
- created_at: 创建时间
- updated_at: 更新时间

### 角色表 (roles)
- id: 主键
- role_code: 角色编码
- role_name: 角色名称
- description: 描述
- status: 状态
- sort_order: 排序
- created_at: 创建时间
- updated_at: 更新时间

### 权限表 (permissions)
- id: 主键
- permission_code: 权限编码
- permission_name: 权限名称
- resource_type: 资源类型
- resource_id: 资源ID
- description: 描述
- status: 状态
- created_at: 创建时间
- updated_at: 更新时间

### 菜单表 (menus)
- id: 主键
- parent_id: 父菜单ID（自引用）
- name: 菜单名称
- icon: 菜单图标
- route: 路由路径
- component: 组件路径
- menu_type: 菜单类型（目录/菜单/按钮）
- permission_code: 权限编码
- sort_order: 排序
- status: 状态
- created_at: 创建时间
- updated_at: 更新时间

### 关联表
- user_roles: 用户角色关联表
- role_permissions: 角色权限关联表

## API 接口

### 菜单管理
- POST /api/v1/menus - 创建菜单
- GET /api/v1/menus - 获取菜单列表
- GET /api/v1/menus/tree - 获取菜单树
- GET /api/v1/menus/{id} - 获取菜单详情
- PUT /api/v1/menus/{id} - 更新菜单
- DELETE /api/v1/menus/{id} - 删除菜单
- GET /api/v1/menus/{id}/children - 获取子菜单

### 认证授权
- POST /api/v1/auth/login - 用户登录
- GET /api/v1/auth/current - 获取当前用户信息
- GET /api/v1/users/me/permissions - 获取用户权限
- GET /api/v1/users/me/roles - 获取用户角色

### RBAC管理
- POST /api/v1/users/{id}/roles - 分配用户角色
- DELETE /api/v1/users/{id}/roles/{role_id} - 撤销用户角色
- POST /api/v1/roles/{id}/permissions - 分配角色权限
- DELETE /api/v1/roles/{id}/permissions/{permission_id} - 撤销角色权限

## 权限指令使用

```vue
<!-- 单个权限检查 -->
<el-button v-permission="'menu:create'">创建菜单</el-button>

<!-- 多个权限检查（拥有任意权限即可） -->
<el-button v-permission="['menu:update', 'menu:delete']">操作</el-button>
```

## 开发说明

### 后端开发
- 遵循 FastAPI 最佳实践
- 使用 SQLAlchemy ORM 进行数据库操作
- 使用 Pydantic 进行数据验证
- 使用依赖注入管理认证授权

### 前端开发
- 使用 TypeScript 保证类型安全
- 使用 Composition API 编写组件
- 使用 Pinia 进行状态管理
- 使用 Element Plus 组件库

## 注意事项

1. **安全性**
   - 生产环境必须修改 SECRET_KEY
   - 密码必须通过 bcrypt 加密存储
   - 所有 API 接口都需要认证（除登录接口）

2. **权限控制**
   - 前端权限控制只是 UI 层面的
   - 后端必须进行严格的权限验证
   - 建议使用 Redis 缓存权限信息以提高性能

3. **菜单管理**
   - 删除菜单会级联删除所有子菜单
   - 更新父菜单时会检测循环引用
   - 同级菜单名称不能重复

## 许可证

MIT License
