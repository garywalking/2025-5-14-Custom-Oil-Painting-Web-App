"""
配置测试文件
测试环境变量和基础配置是否正确加载
"""

from app.core.config import settings

def test_app_settings():
    """测试基础应用配置"""
    # 修改为实际使用的 APP_NAME
    assert settings.APP_NAME == "Custom Oil Painting Web App"
    assert settings.DEBUG is True

def test_database_settings():
    """测试数据库配置"""
    # 修改为检查 DATABASE_URL
    assert settings.DATABASE_URL is not None
    assert settings.DATABASE_URL.startswith("postgresql://")