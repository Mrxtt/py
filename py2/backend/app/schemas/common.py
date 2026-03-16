"""
通用响应模型
"""
from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List, Any
from datetime import datetime

T = TypeVar('T')

class PageData(BaseModel, Generic[T]):
    """分页数据模型"""
    items: List[T] = Field(..., description="数据列表")
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页大小")
    pages: int = Field(..., description="总页数")

class ApiResponse(BaseModel, Generic[T]):
    """统一API响应模型"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="响应消息")
    data: Optional[T] = Field(None, description="响应数据")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": None
            }
        }


class PageResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="响应消息")
    data: PageData[T] = Field(..., description="分页数据")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "items": [],
                    "total": 0,
                    "page": 1,
                    "page_size": 10,
                    "pages": 0
                }
            }
        }
class ErrorResponse(BaseModel):
    """错误响应模型"""
    code: int = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")
    detail: Optional[str] = Field(None, description="错误详情")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 400,
                "message": "Bad Request",
                "detail": "Invalid input data"
            }
        }
