# app/main.py
# FastAPI 应用入口 (FastAPI application entry point) - 更新版
# 核心功能摘要: 初始化 FastAPI 应用，定义根路由，并配置静态文件和 Jinja2 模板。

import uvicorn # 导入 uvicorn，用于运行 FastAPI 应用
from fastapi import FastAPI, Request # 导入 FastAPI 类 和 Request 对象 (用于模板)
from fastapi.staticfiles import StaticFiles # 导入 StaticFiles 用于服务静态文件
from fastapi.templating import Jinja2Templates # 导入 Jinja2Templates 用于模板渲染
from fastapi.responses import HTMLResponse # 导入 HTMLResponse 用于返回 HTML 内容
from app.api.v1 import image_upload # 导入图片上传路由

from app.core.config import settings # 导入应用配置
import os # 导入 os 模块，用于路径操作

# 打印日志，标示 main.py 开始加载
print("LOG: app/main.py - Initializing FastAPI application...")

# --- 路径配置 ---
# 项目根目录的确定方式可以根据实际运行 main.py 的位置调整。
# 如果 main.py 是从 custom_oil_painting_app/ 目录运行 (例如 uvicorn app.main:app)
# 那么 BASE_DIR 就是 custom_oil_painting_app/app
# 如果希望 TEMPLATES_DIR 和 STATIC_DIR 是相对于 custom_oil_painting_app/ 目录
# 则需要进行相应的路径调整。
# 根据你的树形结构，templates 和 static 在 app 目录下。
APP_DIR = os.path.dirname(os.path.abspath(__file__)) # app 目录
TEMPLATES_DIR = os.path.join(APP_DIR, "templates")
STATIC_DIR = os.path.join(APP_DIR, "static")

print(f"LOG: app/main.py - Application directory (APP_DIR): {APP_DIR}")
print(f"LOG: app/main.py - Templates directory (TEMPLATES_DIR): {TEMPLATES_DIR}")
print(f"LOG: app/main.py - Static files directory (STATIC_DIR): {STATIC_DIR}")

# 检查目录是否存在
if not os.path.isdir(TEMPLATES_DIR):
    print(f"LOG: WARNING - Templates directory does not exist: {TEMPLATES_DIR}")
if not os.path.isdir(STATIC_DIR):
    print(f"LOG: WARNING - Static files directory does not exist: {STATIC_DIR}")


# --- FastAPI 应用实例 ---
# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME, # 从配置中读取项目标题
    description="A web application for ordering custom oil paintings.",
    version="0.1.0"
)
print(f"LOG: app/main.py - FastAPI instance created. App Name: {settings.APP_NAME}")


# --- 静态文件挂载 ---
# 挂载静态文件目录。
# "/static" 是 URL 路径，当浏览器请求如 /static/css/styles.css 时，
# FastAPI 会从 `STATIC_DIR` (即 app/static) 目录中查找文件。
# name="static" 允许在模板中使用 url_for('static', path='...') 来生成 URL。
try:
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    print(f"LOG: app/main.py - Static files mounted from '{STATIC_DIR}' at URL '/static'.")
except RuntimeError as e:
    print(f"LOG: ERROR - Failed to mount static files. Directory '{STATIC_DIR}' might not exist or is not accessible: {e}")
    print(f"LOG: app/main.py - Please ensure the static directory '{STATIC_DIR}' exists and contains your CSS/JS files.")


# --- Jinja2 模板配置 ---
# 初始化 Jinja2Templates。
# `TEMPLATES_DIR` (即 app/templates) 是存放 HTML 模板文件的目录。
try:
    templates = Jinja2Templates(directory=TEMPLATES_DIR)
    # 将 settings 对象添加到模板的全局上下文中，这样所有模板都可以访问它
    # 例如在模板中使用 {{ settings.APP_NAME }}
    templates.env.globals["settings"] = settings
    print(f"LOG: app/main.py - Jinja2Templates initialized from directory: {TEMPLATES_DIR}")
except Exception as e:
    print(f"LOG: ERROR - Failed to initialize Jinja2Templates. Directory '{TEMPLATES_DIR}' might not exist: {e}")
    templates = None # 设为 None 以避免后续代码出错，但模板渲染会失败


# --- API 路由 (JSON 响应) ---
@app.get("/api/v1/hello")
async def read_root_api():
    """
    一个简单的 API 端点，返回 JSON。
    """
    print("LOG: API endpoint '/api/v1/hello' accessed.")
    return {"message": "Hello from the Custom Oil Painting API!", "app_name": settings.APP_NAME}


# --- 网页路由 (HTML 响应) ---
@app.get("/", response_class=HTMLResponse, name="read_root_ui") # name 用于 url_for
async def read_root_ui(request: Request):
    """
    根路径 ("/") 的处理函数，返回 HTML 页面。
    使用 Jinja2 模板渲染 index.html。
    """
    print("LOG: UI endpoint '/' (read_root_ui) accessed.")
    if not templates:
        print("LOG: ERROR - Templates not initialized, cannot render index.html.")
        return HTMLResponse(content="<h1>Error: Templates not configured.</h1><p>Please check server logs.</p>", status_code=500)

    # 从 API 获取一些数据来传递给模板 (示例)
    api_data = await read_root_api() # 调用上面的 API 端点

    # 准备传递给模板的上下文数据
    context = {
        "request": request, # Request 对象是 Jinja2Templates 必需的
        "page_title": "Homepage",
        "welcome_message": f"Welcome to {settings.APP_NAME}",
        "api_message": api_data.get("message", "Could not load API message.") # 从 API 调用获取消息
    }
    print(f"LOG: Rendering index.html with context: page_title='{context['page_title']}'")
    try:
        return templates.TemplateResponse("index.html", context)
    except Exception as e:
        print(f"LOG: ERROR - Failed to render template 'index.html': {e}")
        # 可以考虑返回一个更友好的错误页面
        return HTMLResponse(content=f"<h1>Error rendering page</h1><p>Details: {e}</p>", status_code=500)

# 为了向后兼容或提供一个纯 API 的根路径，可以保留原来的 /api 路由
# 或者将原来的 "/" 重命名或移除，取决于你的需求。
# 这里我将原来的 @app.get("/") 改名为 @app.get("/api/info") 或类似
@app.get("/api/info", name="read_root_api_info") # 确保 name 不冲突
async def read_root_original_json():
    """
    原先的根路由，返回 JSON。现在路径改为 /api/info。
    """
    print("LOG: Original API endpoint '/api/info' was accessed.")
    return {"message": "Welcome to the Custom Oil Painting Web App (JSON API Info)!", "version": app.version}


# --- API 路由注册 ---
# 注册图片上传路由
app.include_router(image_upload.router, prefix="/api/v1", tags=["upload"])

# --- 注册路由 ---
app.include_router(image_upload.router, prefix="/api/v1")

print("LOG: app/main.py - Routes registered successfully.")


# --- 应用启动 (用于直接运行此文件) ---
if __name__ == "__main__":
    # 打印日志，标示开发服务器启动
    print("LOG: app/main.py - Starting Uvicorn server for development at http://localhost:8000")
    # reload_dirs=["app"] 可以让 uvicorn 监控 app 文件夹下的变动，更精确。
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=[APP_DIR])

print("LOG: app/main.py - Script loaded and FastAPI app configured.")