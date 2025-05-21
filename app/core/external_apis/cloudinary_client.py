import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from typing import List, Dict, Union
import os
import mimetypes
from app.core.config import Settings

# 支持的图片格式
ALLOWED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.heic', '.heif'}

class CloudinaryClient:
    def __init__(self):
        # 创建 settings 实例
        settings = Settings()
        # 初始化 Cloudinary 配置
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )

    @staticmethod
    def is_valid_format(filename: str) -> bool:
        """
        验证文件格式是否支持
        """
        ext = os.path.splitext(filename)[1].lower()
        return ext in ALLOWED_FORMATS

    async def upload_image(self, file: UploadFile) -> Dict[str, Union[bool, str, Dict]]:
        """
        上传图片到 Cloudinary
        
        Args:
            file: UploadFile 对象

        Returns:
            Dict 包含:
                success: 是否上传成功
                message: 提示信息
                data: 上传成功时返回的数据（包含URL等信息）
        """
        if not self.is_valid_format(file.filename):
            return {
                "success": False,
                "message": f"不支持的文件格式。支持的格式：{', '.join(ALLOWED_FORMATS)}",
                "data": None
            }

        try:
            # 读取文件内容
            contents = await file.read()
            
            # 上传到 Cloudinary
            result = cloudinary.uploader.upload(
                contents,
                folder="custom_oil_paintings",  # 在 Cloudinary 中的存储文件夹
                resource_type="auto"
            )

            # 不使用 await 的方式重置文件指针
            file.seek(0)

            return {
                "success": True,
                "message": "图片上传成功",
                "data": {
                    "url": result["secure_url"],
                    "public_id": result["public_id"],
                    "format": result["format"],
                    "width": result["width"],
                    "height": result["height"]
                }
            }

        except Exception as e:
            # 不使用 await 的方式重置文件指针
            file.seek(0)
            return {
                "success": False,
                "message": f"上传失败: {str(e)}",
                "data": None
            }