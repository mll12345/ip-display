FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

# 复制所有文件
COPY . .

# 暴露端口
EXPOSE 80

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 启动命令
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:80", "server:app"]