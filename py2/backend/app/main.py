"""
FastAPI 主应用
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .core.config import Settings
from .core.database import get_db
from .routers import (
    menu_router,
    rbac_router,
    user_router,
    role_router,
    permission_router,
)
from .dependencies.auth import get_current_user
from .models import User
from .schemas.rbac import UserResponse
from .schemas.common import ApiResponse

settings = Settings()

# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="无限层菜单动态添加管理系统",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
# app.include_router(Settings)
app.include_router(menu_router)
app.include_router(rbac_router)
app.include_router(user_router)
app.include_router(role_router)
app.include_router(permission_router)


# 修复 Settings 中的 get_current_user_info 路由
@app.get(
    "/api/v1/auth/current",
    response_model=ApiResponse[UserResponse],
    summary="获取当前用户信息",
)
async def get_current_user_info(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    获取当前登录用户信息

    - 需要认证
    """
    # 刷新用户数据
    db.refresh(current_user)
    user_response = UserResponse.model_validate(current_user)

    return ApiResponse(code=200, message="查询成功", data=user_response)


@app.get("/", summary="根路径")
async def root():
    """根路径"""
    return {
        "message": "无限层菜单管理系统 API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health", summary="健康检查")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
