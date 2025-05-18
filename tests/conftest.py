"""
测试配置文件
主要用于设置测试环境和提供测试固件(fixtures)
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.config import settings
from app.db.session import Base

# 创建测试数据库引擎（使用SQLite内存数据库）
SQLALCHEMY_TEST_DATABASE_URL = "sqlite://"
test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def test_app():
    """创建测试用的FastAPI应用实例"""
    return app

@pytest.fixture(scope="session")
def test_client():
    """创建测试用的客户端"""
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="function")
def test_db():
    """创建测试数据库会话，每个测试函数都会获得一个新的会话"""
    Base.metadata.create_all(bind=test_engine)  # 创建所有表
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)  # 清理所有表