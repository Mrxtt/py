@echo off
chcp 65001 >nul
echo ==========================================
echo   无限层菜单管理系统
echo ==========================================

REM 检查是否安装了必要的工具
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 需要安装 Python3
    pause
    exit /b 1
)

npm --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 需要安装 Node.js 和 npm
    pause
    exit /b 1
)

REM 后端启动
echo.
echo [1/2] 启动后端服务...
cd backend

REM 检查虚拟环境
if not exist "..\venv" (
    echo 创建虚拟环境...
    python -m venv ..\venv
)

REM 激活虚拟环境
call ..\venv\Scripts\activate.bat

REM 安装依赖
echo 安装后端依赖...
pip install -r requirements.txt

REM 检查数据库配置
if not exist ".env" (
    echo 创建环境配置文件...
    copy .env.example .env
    echo 警告: 请编辑 backend\.env 文件，配置数据库连接信息
)

REM 初始化数据库
echo 初始化数据库...
python init_db.py

REM 启动后端服务
echo 启动后端服务 (端口 8000)...
start "后端服务" python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

cd ..

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 前端启动
echo.
echo [2/2] 启动前端服务...
cd frontend

REM 安装依赖
if not exist "node_modules" (
    echo 安装前端依赖...
    call npm install
)

REM 检查环境配置
if not exist ".env" (
    echo 创建环境配置文件...
    copy .env.example .env
)

REM 启动前端服务
echo 启动前端服务 (端口 5173)...
start "前端服务" npm run dev

cd ..

echo.
echo ==========================================
echo   启动完成！
echo ==========================================
echo 后端服务: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo 前端应用: http://localhost:5173
echo.
echo 请关闭命令窗口以停止服务
echo ==========================================

pause
