"""
数据库初始化脚本
创建所有数据库表
"""

import sys
import os
from sqlalchemy.exc import SQLAlchemyError


# 添加项目根目录到Python路径
project_root = sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from app.core.database import engine, Base
    from app.models import User, Role, Permission, Menu
except ModuleNotFoundError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)


def create_tables():
    """创建所有数据库表"""
    print("开始创建数据库表...")

    try:
        # 创建所有表
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as e:
        print(f"❌ 数据库表创建失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        sys.exit(1)

    print("✅ 数据库表创建成功！")
    print("\n已创建的表：")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")


if __name__ == "__main__":
    # 调用加载
    create_tables()
