# custom_oil_painting_app/Dockerfile
# Docker 构建文件 (Docker build instructions)
# 核心功能摘要: 定义如何构建应用的 Docker 镜像。

# 阶段 1: 构建基础镜像
# 使用官方 Python 3.11 slim 镜像作为基础。
# "slim" 版本通常更小，适合生产环境。
FROM python:3.9-slim
# 声明作者信息 (可选)
LABEL maintainer="garywalking@gmail.com"

# 设置环境变量
# PYTHONUNBUFFERED=1: 确保 Python 输出（如 print 语句）直接发送到终端，方便 Docker 日志查看。
# PYTHONDONTWRITEBYTECODE=1: 阻止 Python 生成 .pyc 文件，在容器环境中通常不需要。
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 设置工作目录
# 在容器内创建一个名为 /app 的工作目录，后续的命令将在此目录下执行。
WORKDIR /app

# 安装系统依赖
# 如果你的项目需要一些系统级别的库（例如，Pillow 可能需要 libjpeg-dev 或 zlib1g-dev），
# 你需要在这里通过 apt-get 安装它们。
# 对于 psycopg2-binary，通常不需要额外的系统库，因为它自带了编译好的二进制文件。
# 对于 Pillow，它可能需要一些图像处理相关的库，例如：
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libjpeg-dev \
#     zlib1g-dev \
#     && rm -rf /var/lib/apt/lists/*
# 目前我们先不加，如果后续 Pillow 报错，再添加。
# 打印日志，标示系统依赖安装步骤（如果实际执行了安装）
# RUN echo "LOG: Installing system dependencies if any..."

# 阶段 2: 安装 Python 依赖
# 将 requirements.txt 文件复制到工作目录。
COPY requirements.txt .
# 打印日志，标示 Python 依赖安装开始
RUN echo "LOG: Installing Python dependencies from requirements.txt..."
# 配置 apt 使用中科大镜像源
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

# 更新系统并安装基础工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 配置 pip 使用中科大镜像源
RUN pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/ \
    && pip config set global.trusted-host pypi.mirrors.ustc.edu.cn \
    && pip install --upgrade pip

# 使用 pip 安装 requirements.txt 中定义的 Python 包。
# --no-cache-dir: 不缓存下载的包，以减小镜像体积。
# -r requirements.txt: 从指定文件安装。
RUN pip install --no-cache-dir -r requirements.txt
# 打印日志，标示 Python 依赖安装完成
RUN echo "LOG: Python dependencies installed."

# 阶段 3: 复制应用代码
# 将当前目录下的所有文件（Dockerfile 所在目录，即项目根目录）复制到容器的 /app 目录。
# 注意：为了更有效地利用 Docker 的层缓存，通常建议先复制依赖文件 (requirements.txt) 并安装，
# 然后再复制应用代码。这样，如果只有代码改变而依赖不变，Docker 可以重用之前的依赖层。
# 我们这里将整个 app 目录复制过去。如果你的项目根目录还有其他配置文件需要被应用读取，也应一并考虑。
# 根据你的项目结构，我们应该复制 app 目录到容器的 /app/app 目录，或者直接将 app 目录的内容复制到 /app。
# 假设 FastAPI 应用在 custom_oil_painting_app/app/main.py
COPY ./app /app/app
# 打印日志，标示应用代码复制完成
RUN echo "LOG: Application code copied to /app/app."

# 暴露端口
# 声明容器将监听的端口。这只是一个元数据声明，实际端口映射在 docker run 或 docker-compose.yml 中完成。
# FastAPI 默认运行在 8000 端口 (由 uvicorn 控制)。
EXPOSE 8000

# 定义容器启动时执行的命令
# 使用 uvicorn 运行 FastAPI 应用。
# "app.main:app": 指向 app 文件夹下的 main.py 文件中的 app FastAPI 实例。
# --host 0.0.0.0: 使应用可以从容器外部访问。
# --port 8000: 指定监听的端口。
# --reload: 在开发环境中，当代码更改时自动重新加载应用。生产环境应移除 --reload。
# 根据项目结构，FastAPI 应用实例在 app/main.py 中，所以路径是 app.main:app
# 打印日志，标示容器即将启动
CMD echo "LOG: Starting FastAPI application with Uvicorn..." && uvicorn app.main:app --host 0.0.0.0 --port 8000
# 对于生产环境，通常不使用 --reload。例如:
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]