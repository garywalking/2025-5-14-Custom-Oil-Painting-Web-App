import pytest
from unittest.mock import Mock, patch
from fastapi import UploadFile
from app.core.external_apis.cloudinary_client import CloudinaryClient

@pytest.fixture
def cloudinary_client():
    return CloudinaryClient()

def test_is_valid_format():
    client = CloudinaryClient()
    
    # 测试有效格式
    assert client.is_valid_format("test.jpg") is True
    assert client.is_valid_format("test.jpeg") is True
    assert client.is_valid_format("test.png") is True
    assert client.is_valid_format("test.webp") is True
    assert client.is_valid_format("test.bmp") is True
    assert client.is_valid_format("test.heic") is True
    assert client.is_valid_format("test.heif") is True
    
    # 测试无效格式
    assert client.is_valid_format("test.gif") is False
    assert client.is_valid_format("test.txt") is False
    assert client.is_valid_format("test") is False

@pytest.mark.asyncio
async def test_upload_image_invalid_format(cloudinary_client):
    # 创建模拟的 UploadFile 对象
    mock_file = Mock(spec=UploadFile)
    mock_file.filename = "test.txt"
    
    result = await cloudinary_client.upload_image(mock_file)
    
    assert result["success"] is False
    assert "不支持的文件格式" in result["message"]
    assert result["data"] is None

@pytest.mark.asyncio
@patch('cloudinary.uploader.upload')
async def test_upload_image_success(mock_upload, cloudinary_client):
    # 模拟 Cloudinary 上传响应
    mock_upload.return_value = {
        "secure_url": "https://example.com/image.jpg",
        "public_id": "test_public_id",
        "format": "jpg",
        "width": 100,
        "height": 100
    }
    
    # 创建异步模拟对象
    class AsyncMock:
        async def read(self):
            return b"test_content"
        async def seek(self, position):
            return None
        @property
        def filename(self):
            return "test.jpg"
    
    mock_file = AsyncMock()
    result = await cloudinary_client.upload_image(mock_file)
    
    assert result["success"] is True
    assert result["message"] == "图片上传成功"
    assert result["data"]["url"] == "https://example.com/image.jpg"
    assert result["data"]["public_id"] == "test_public_id"
    assert result["data"]["format"] == "jpg"
    assert result["data"]["width"] == 100
    assert result["data"]["height"] == 100

@pytest.mark.asyncio
@patch('cloudinary.uploader.upload')
async def test_upload_image_failure(mock_upload, cloudinary_client):
    # 模拟上传失败
    mock_upload.side_effect = Exception("Upload failed")
    
    # 创建异步模拟对象
    class AsyncMock:
        async def read(self):
            return b"test_content"
        async def seek(self, position):
            return None
        @property
        def filename(self):
            return "test.jpg"
    
    mock_file = AsyncMock()
    result = await cloudinary_client.upload_image(mock_file)
    
    assert result["success"] is False
    assert "Upload failed" in result["message"]
    assert result["data"] is None
