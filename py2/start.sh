#!/bin/bash

# 无限层菜单管理系统启动脚本

echo "=========================================="
echo "  无限层菜单管理系统"
echo "=========================================="

# 检查是否安装了必要的工具
command -v python3 >/dev/null 2>&1 || { echo "错误: 需要安装 Python3"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "错误: 需要安装 Node.js 和 npm"; exit 1; }

# 后端启动
echo ""
echo "[1/2] 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "../venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv ../venv
fi

# 激活虚拟环境
source ../venv/bin/activate

# 安装依赖
echo "安装后端依赖..."
pip install -r requirements.txt

# 检查数据库配置
if [ ! -f ".env" ]; then
    echo "创建环境配置文件..."
    cp .env.example .env
    echo "警告: 请编辑 backend/.env 文件，配置数据库连接信息"
fi

# 初始化数据库
echo "初始化数据库..."
python init_db.py

# 启动后端服务
echo "启动后端服务 (端口 8000)..."
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ..

# 等待后端启动
sleep 3

# 前端启动
echo ""
echo "[2/2] 启动前端服务..."
cd frontend

# 安装依赖
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

# 检查环境配置
if [ ! -f ".env" ]; then
    echo "创建环境配置文件..."
    cp .env.example .env
fi

# 启动前端服务
echo "启动前端服务 (端口 5173)..."
npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo "=========================================="
echo "  启动完成！"
echo "=========================================="
echo "后端服务: http://localhost:8000"
echo "API 文档: http://localhost:8000/docs"
echo "前端应用: http://localhost:5173"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo "=========================================="

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait
