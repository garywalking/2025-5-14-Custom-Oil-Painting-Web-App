from fastapi import APIRouter, UploadFile, File
from app.core.external_apis.cloudinary_client import CloudinaryClient

router = APIRouter()
cloudinary_client = CloudinaryClient()

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    """
    处理图片上传
    
    Args:
        file: 上传的图片文件
    
    Returns:
        包含上传结果的字典
    """
    result = await cloudinary_client.upload_image(file)
    return result
