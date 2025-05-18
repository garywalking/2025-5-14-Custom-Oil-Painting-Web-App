# app/core/config.py
# 应用配置 (Application settings from env vars)
# 核心功能摘要: 定义应用的基础配置，并从环境变量中加载敏感或环境特定的设置。

import os  # 导入 os 模块，用于访问环境变量
from dotenv import load_dotenv  # 从 python-dotenv 库导入 load_dotenv 函数
# 从 pydantic-settings 导入 BaseSettings，用于类型安全的配置管理
from pydantic_settings import BaseSettings
from typing import Optional  # 导入 Optional，用于可选类型的注解

# 项目的根目录路径
# os.path.dirname 获取当前文件 (config.py) 所在的目录 (app/core)
# os.path.dirname(...) 再次获取上一级目录 (app)
# os.path.dirname(...) 再次获取上一级目录 (custom_oil_painting_app)
# 这是为了确保无论从哪里运行脚本，都能正确找到 .env 文件。
# 注意：根据你的实际项目结构，你可能需要调整这里的层级。
# 假设 .env 文件与 manage.py 或顶层项目文件夹同级。
# 如果项目结构是 custom_oil_painting_app/.env，那么下面这样是对的。
# 如果是 custom_oil_painting_app/app/.env，则需要调整。
# 根据你的 "项目树形结构（gemini版）.txt"，.env 文件在顶级目录。
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
ENV_FILE_PATH = os.path.join(PROJECT_ROOT_DIR, ".env")

# 打印日志，显示 .env 文件的预期路径，方便调试
print(f"LOG: Attempting to load .env file from: {ENV_FILE_PATH}")

# 加载 .env 文件中的环境变量
# load_dotenv 会查找指定路径的 .env 文件，并将其中的键值对加载到环境变量中。
# override=True 表示如果 .env 文件中的变量与系统已有的环境变量冲突，则优先使用 .env 文件中的值。
if os.path.exists(ENV_FILE_PATH):
    load_dotenv(ENV_FILE_PATH, override=True)
    print(f"LOG: Successfully loaded .env file from: {ENV_FILE_PATH}")
else:
    print(
        f"LOG: Warning - .env file not found at: {ENV_FILE_PATH}. Using system environment variables or defaults.")


# 定义一个继承自 BaseSettings 的配置类
# Pydantic 的 BaseSettings 会自动从环境变量中读取与类属性同名的值。
# 它还会进行类型转换和验证。
class Settings(BaseSettings):
    """
    应用配置类。
    属性会从环境变量中自动加载和验证。
    """
    # 应用名称，可以从环境变量 APP_NAME 读取，如果未设置，则使用默认值。
    APP_NAME: str = os.getenv(
        "APP_NAME", "Custom Oil Painting Web App")  # [cite: 139]
    # 调试模式，从环境变量 DEBUG 读取，转换为布尔值。
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"  # [cite: 139]

    # 数据库连接 URL，从环境变量 DATABASE_URL 读取。
    # 这是一个敏感信息，强烈建议通过环境变量配置。
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")  # [cite: 139]

    # Redis 连接 URL，用于 Celery。
    REDIS_URL: str = os.getenv(
        "REDIS_URL", "redis://localhost:6379/0")  # [cite: 139]

    # Cloudinary 配置
    CLOUDINARY_CLOUD_NAME: Optional[str] = os.getenv(
        "CLOUDINARY_CLOUD_NAME")  # [cite: 139]
    CLOUDINARY_API_KEY: Optional[str] = os.getenv(
        "CLOUDINARY_API_KEY")  # [cite: 139]
    CLOUDINARY_API_SECRET: Optional[str] = os.getenv(
        "CLOUDINARY_API_SECRET")  # [cite: 139]

    # Stability AI 配置
    STABILITY_API_KEY: Optional[str] = os.getenv(
        "STABILITY_API_KEY")  # [cite: 139]
    # STABILITY_API_URL: Optional[str] = os.getenv("STABILITY_API_URL") # [cite: 139] # 根据需求书，这个似乎是固定的

    # Stripe 配置
    STRIPE_PUBLISHABLE_KEY: Optional[str] = os.getenv(
        "STRIPE_PUBLISHABLE_KEY")  # [cite: 139]
    STRIPE_SECRET_KEY: Optional[str] = os.getenv(
        "STRIPE_SECRET_KEY")  # [cite: 139]
    STRIPE_WEBHOOK_SECRET: Optional[str] = os.getenv(
        "STRIPE_WEBHOOK_SECRET")  # [cite: 139]

    # Resend (邮件服务) 配置
    RESEND_API_KEY: Optional[str] = os.getenv("RESEND_API_KEY")  # [cite: 139]
    EMAIL_FROM_ADDRESS: Optional[str] = os.getenv(
        "EMAIL_FROM_ADDRESS", "noreply@example.com")  # [cite: 139]

    # Pydantic 的 model_config 用于配置 BaseSettings 的行为
    # case_sensitive = True 表示环境变量名称必须与属性名称大小写完全匹配。
    # env_file = ENV_FILE_PATH  # 指定 .env 文件的路径 (Pydantic V2 推荐在 load_dotenv 中处理)
    # env_file_encoding = 'utf-8' # 指定 .env 文件的编码

    class Config:
        env_file = ENV_FILE_PATH  # 告诉 Pydantic 从哪里加载 .env 文件
        env_file_encoding = 'utf-8'
        extra = 'ignore'  # 如果 .env 文件中有 Settings 类未定义的变量，则忽略它们


# 创建 Settings 类的实例，这个实例可以在应用的其他部分导入和使用。
settings = Settings()

# 打印日志，显示加载的配置值（注意：在生产环境中避免打印敏感信息）
# 为了安全，我们只打印部分非敏感配置或确认配置已加载
print(f"LOG: Application Name from config: {settings.APP_NAME}")
print(f"LOG: Debug Mode from config: {settings.DEBUG}")
if settings.DATABASE_URL:
    print("LOG: DATABASE_URL is configured.")
else:
    print("LOG: Warning - DATABASE_URL is NOT configured.")

if settings.CLOUDINARY_CLOUD_NAME:
    print("LOG: Cloudinary is configured.")
else:
    print("LOG: Warning - Cloudinary is NOT configured.")
