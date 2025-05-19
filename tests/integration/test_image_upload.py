import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def test_upload_endpoint_invalid_file():
    # 创建一个无效格式的文件
    file_content = b"test content"
    files = {
        "file": ("test.txt", io.BytesIO(file_content), "text/plain")
    }
    
    response = client.post("/api/v1/upload/", files=files)
    assert response.status_code == 200  # API 返回 200 但带有错误信息
    
    data = response.json()
    assert data["success"] is False
    assert "不支持的文件格式" in data["message"]

def test_upload_endpoint_no_file():
    response = client.post("/api/v1/upload/")
    assert response.status_code == 422  # FastAPI 的验证错误

def test_upload_endpoint_empty_file():
    files = {
        "file": ("test.jpg", io.BytesIO(b""), "image/jpeg")
    }
    
    response = client.post("/api/v1/upload/", files=files)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is False
