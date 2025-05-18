# app/db/session.py
# 数据库会话管理 (Database session management)
# 核心功能摘要: 配置数据库连接引擎和会话创建。

from sqlalchemy import create_engine  # 从 SQLAlchemy 导入 create_engine，用于创建数据库引擎
# 从 SQLAlchemy.orm 导入 sessionmaker (创建会话工厂) 和 Session (会话类型)
from sqlalchemy.orm import sessionmaker, Session
# 从 SQLAlchemy.ext.declarative 导入 declarative_base，用于定义 ORM 模型
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings  # 导入应用配置 (settings 实例，包含了 DATABASE_URL)
from typing import Generator  # 导入 Generator 类型，用于类型注解

# 打印日志，显示从配置中获取的 DATABASE_URL
# 注意：在生产环境中，避免直接打印完整的数据库 URL，除非用于调试且确保安全。
# 打印部分 URL 以避免泄露密码
print(
    f"LOG: session.py - DATABASE_URL from settings: {settings.DATABASE_URL[:settings.DATABASE_URL.find('@') if '@' in settings.DATABASE_URL else len(settings.DATABASE_URL)]}...")

# 检查 DATABASE_URL 是否已配置
if not settings.DATABASE_URL:
    print("LOG: FATAL ERROR - DATABASE_URL is not configured in environment variables or .env file.")
    print("LOG: Please set DATABASE_URL, e.g., postgresql://user:password@host:port/dbname")
    # 在实际应用中，这里可能应该抛出异常或退出程序
    # raise ValueError("DATABASE_URL is not configured.")
    # 为了让程序能继续进行其他文件的生成，这里仅打印错误。
    # 但数据库相关操作会失败。
    SQLALCHEMY_DATABASE_URL = "sqlite:///./temp.db"  # 临时备用，避免程序完全崩溃
    print(
        f"LOG: Using temporary in-memory SQLite database: {SQLALCHEMY_DATABASE_URL} due to missing DATABASE_URL.")
else:
    SQLALCHEMY_DATABASE_URL = str(settings.DATABASE_URL)  # 确保是字符串类型

# 创建 SQLAlchemy 引擎
# create_engine 是 SQLAlchemy ORM 的入口点，它代表了与数据库的连接。
# connect_args 是特定于数据库驱动程序的参数。
# 对于 PostgreSQL (psycopg2), "options": "-c timezone=UTC" 可以设置会话时区为 UTC。
# pool_pre_ping=True: 启用连接池的 "pre-ping" 功能，它会在每次从池中检出连接之前测试其活性。
# 这有助于处理数据库连接可能因网络问题或数据库重启而失效的情况。
try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        # connect_args={"options": "-c timezone=UTC"}, # 根据需要设置时区
        pool_pre_ping=True,
        echo=settings.DEBUG  # 如果 DEBUG 为 True，则 SQLAlchemy 会打印所有执行的 SQL 语句，方便调试
    )
    print(
        f"LOG: SQLAlchemy engine created for URL (details hidden for security). Echo SQL: {settings.DEBUG}")
except Exception as e:
    print(f"LOG: Error creating SQLAlchemy engine: {e}")
    # 如果引擎创建失败，后续依赖此引擎的代码会出错
    # 实际应用中可能需要更健壮的错误处理
    engine = None  # 将 engine 设为 None，以便后续代码可以检查


# 创建 SessionLocal 类 (会话工厂)
# sessionmaker 是一个工厂，用于创建新的 Session 对象。
# autocommit=False: 在事务块中，更改不会自动提交到数据库，需要显式调用 commit()。
# autoflush=False: 在查询之前，不会自动将挂起的更改刷新（发送）到数据库。
# bind=engine: 将此会话工厂绑定到我们创建的数据库引擎。
if engine:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("LOG: SQLAlchemy SessionLocal created and bound to engine.")
else:
    SessionLocal = None  # 如果引擎创建失败，SessionLocal 也无法创建
    print("LOG: SQLAlchemy SessionLocal could not be created due to engine initialization failure.")


# 创建 ORM 模型的基础类
# 所有数据库模型类都将继承自这个 Base 类。
Base = declarative_base()
print("LOG: SQLAlchemy Base for declarative models created.")


# 数据库会话依赖项 (用于 FastAPI)
# 这是一个生成器函数，将用作 FastAPI 的依赖项，为每个请求提供一个数据库会话。
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI 依赖项，用于获取数据库会话。
    它确保数据库会话在请求处理完成后正确关闭。

    Yields:
        Generator[Session, None, None]: 数据库会话对象。
    """
    if SessionLocal is None:
        print(
            "LOG: ERROR in get_db - SessionLocal is None. Database not properly configured.")
        # 实际应用中，这里应该引发一个 HTTP 异常，例如 503 Service Unavailable
        # from fastapi import HTTPException, status
        # raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database not configured")
        # 为了演示，这里暂时 yield None，但这会导致后续使用 db 的地方出错。
        yield None  # 这会导致使用 db 的地方出错
        return

    print("LOG: get_db - Creating database session.")
    db = SessionLocal()  # 从会话工厂创建一个新的会话实例
    try:
        yield db  # 将会话提供给路径操作函数
    except Exception as e:
        print(
            f"LOG: get_db - Exception during database session, rolling back: {e}")
        db.rollback()  # 如果在处理请求时发生异常，回滚事务
        raise  # 重新抛出异常，以便 FastAPI 可以处理它
    finally:
        print("LOG: get_db - Closing database session.")
        db.close()  # 无论成功还是失败，最终都关闭会话，释放连接回连接池

# 你可以在这里添加一个函数来创建所有表（如果需要的话）
# 例如，在应用启动时调用


def create_db_and_tables():
    """
    (可选) 根据 Base 中定义的模型在数据库中创建所有表。
    通常在应用启动时或通过迁移工具 (如 Alembic) 管理。
    """
    if engine is None:
        print("LOG: create_db_and_tables - Engine is None. Cannot create tables.")
        return

    try:
        print("LOG: create_db_and_tables - Attempting to create database tables (if they don't exist).")
        # Base.metadata.create_all(bind=engine)
        # 注意: 在实际项目中，数据库迁移通常由 Alembic 这样的工具管理，而不是直接调用 create_all。
        # 直接调用 create_all 适用于简单项目或快速原型开发。
        # 如果表已存在，create_all 通常不会修改它们。
        print("LOG: create_db_and_tables - Table creation process (if implemented by create_all) would be here.")
        print("LOG: For production, use Alembic for migrations instead of Base.metadata.create_all().")
    except Exception as e:
        print(f"LOG: Error creating database tables: {e}")

# 如果你想在模块加载时就尝试创建表（仅用于非常简单的场景或测试）
# if settings.DEBUG and engine: # 只在调试模式下且引擎成功创建时执行
#    create_db_and_tables()
