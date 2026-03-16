"""
认证相关 API 路由
"""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..core.security import verify_password, get_password_hash, create_access_token
from ..core.config import Settings
from ..models import User
from ..models.enums import UserStatus
from ..schemas.rbac import LoginRequest, LoginResponse, UserResponse
from ..schemas.common import ApiResponse

# 创建路由器
router = APIRouter(prefix="/api/v1/auth", tags=["认证"])


@router.post("/login", response_model=ApiResponse[LoginResponse], summary="用户登录")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录

    - 验证用户名和密码
    - 返回JWT访问令牌
    """
    # 查询用户
    user = db.query(User).filter(User.username == login_data.username).first()

    print("测试：" + get_password_hash(login_data.password))

    # 验证用户是否存在
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
        )

    # 验证密码
    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
        )

    # 检查用户状态
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="用户已被禁用"
        )

    # 更新最后登录时间
    user.last_login_at = datetime.utcnow()
    db.commit()

    # 生成访问令牌
    access_token_expires = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    # 返回登录响应
    login_response = LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user),
    )

    return ApiResponse(code=200, message="登录成功", data=login_response)


@router.get(
    "/current", response_model=ApiResponse[UserResponse], summary="获取当前用户信息"
)
async def get_current_user_info(
    current_user: User = Depends(lambda: None),  # 这里需要从依赖获取
):
    """
    获取当前登录用户信息

    - 需要认证
    """
    # 这个路由会在主应用中通过依赖注入实现
    pass
