from fastapi import APIRouter, UploadFile, File
from app.services.image_service import ImageService

router = APIRouter()
image_service = ImageService()

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    """
    处理图片上传
    
    Args:
        file: 上传的图片文件
    
    Returns:
        包含上传结果的字典
    """
    result = await image_service.upload_image(file)
    return result
