from fastapi import UploadFile
from app.core.external_apis.cloudinary_client import CloudinaryClient
from app.schemas.image import ImageUploadResponse, ImageMetadata

class ImageService:
    def __init__(self):
        self.cloudinary_client = CloudinaryClient()

    async def upload_image(self, file: UploadFile) -> ImageUploadResponse:
        """
        处理图片上传
        
        Args:
            file: 上传的文件对象
            
        Returns:
            ImageUploadResponse: 上传结果
        """
        # 调用 Cloudinary 客户端上传图片
        result = await self.cloudinary_client.upload_image(file)
        
        if not result["success"]:
            return ImageUploadResponse(
                success=False,
                message=result["message"]
            )
            
        # 转换为 ImageMetadata 模型
        metadata = ImageMetadata(
            url=result["data"]["url"],
            public_id=result["data"]["public_id"],
            format=result["data"]["format"],
            width=result["data"]["width"],
            height=result["data"]["height"]
        )
        
        return ImageUploadResponse(
            success=True,
            message="图片上传成功",
            data=metadata.model_dump()
        )
