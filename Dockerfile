# 使用官方 Python 运行时作为父镜像
FROM --platform=linux/amd64 python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器的 /app 中
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口 8000 供 FastAPI 使用
EXPOSE 8000

# 运行 FastAPI 应用
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
