from pydantic import BaseModel
from typing import Optional

class ImageUploadResponse(BaseModel):
    """图片上传响应的数据结构"""
    success: bool
    message: str
    data: Optional[dict] = None

class ImageMetadata(BaseModel):
    """图片元数据"""
    url: str
    public_id: str
    format: str
    width: int
    height: int
