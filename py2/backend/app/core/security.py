"""
安全相关工具类
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..core.config import Settings
import bcrypt

print(bcrypt.__version__)
# ========================
# 密码加密上下文配置
# ========================
# 支持 bcrypt 和 argon2，如果想迁移到 argon2 只需调整 schemes 顺序
pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"  # 可以改为 ["argon2", "bcrypt"]
)

# bcrypt 最大支持 72 字节
BCRYPT_MAX_BYTES = 72


def _truncate_password(password: str) -> str:
    """
    截断密码，保证 bcrypt 不报错
    """
    # UTF-8 编码后截断为 72 字节
    truncated_bytes = password.encode("utf-8")[:BCRYPT_MAX_BYTES]
    # 再解码回字符串，如果有不完整字符，忽略掉
    return truncated_bytes.decode("utf-8", "ignore")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码

    Args:
        plain_password: 明文密码
        hashed_password: 加密密码

    Returns:
        是否匹配
    """
    new_hash = pwd_context.hash(plain_password)
    print("hash密码： " + new_hash)

    safe_password = _truncate_password(plain_password)
    return pwd_context.verify(safe_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    加密密码

    Args:
        password: 明文密码

    Returns:
        加密后的密码
    """
    safe_password = _truncate_password(password)
    return pwd_context.hash(safe_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌

    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量

    Returns:
        JWT令牌
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    解码访问令牌

    Args:
        token: JWT令牌

    Returns:
        解码后的数据
    """
    try:
        payload = jwt.decode(
            token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
