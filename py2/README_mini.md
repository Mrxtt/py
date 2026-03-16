
```bash
## 安装虚拟环境
python3.12 -m venv venv1 
## 激活并使用虚拟环境
source venv1/bin/activate
## 安装依赖
pip install -r requirements.txt

## 创建表 修改配置
cp .env.example .env

## 初始化创建表
python3.12 init_db.py

### 启动 
python3.12 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

settings = Settings()
```









## 退出虚拟环境
```bash
deactivate
```

## 重新导入依赖
```bash
pip freeze > requirements.txt
```