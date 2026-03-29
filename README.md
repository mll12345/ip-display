# IP地址显示服务

一个简单的Web服务，自动显示访问者的公网IP地址，无需依赖第三方API。

## 功能特点

- ✅ 直接从服务器获取访问者IP
- ✅ 支持代理、CDN等场景
- ✅ 现代化的UI设计
- ✅ 响应式布局，适配移动端
- ✅ 无需第三方API服务

## 快速开始

### 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 启动服务器：
```bash
python server.py
```

3. 在浏览器中访问：
```
http://127.0.0.1:5000
```

## 部署到服务器

### 使用 Gunicorn（推荐）

1. 安装 Gunicorn：
```bash
pip install gunicorn
```

2. 启动服务：
```bash
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

### 使用 Nginx + Gunicorn

配置 Nginx 反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 使用 Docker

创建 `Dockerfile`：

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "server:app"]
```

构建并运行：

```bash
docker build -t ip-display .
docker run -p 5000:5000 ip-display
```

## 环境变量

可通过环境变量配置：

- `PORT`: 服务器端口（默认：5000）
- `HOST`: 服务器地址（默认：0.0.0.0）

## 注意事项

- 确保服务器防火墙开放相应端口
- 生产环境建议使用 Gunicorn 或 uWSGI
- 配置好 HTTPS 证书保证安全传输

## 技术栈

- 后端：Python Flask
- 前端：原生 HTML/CSS/JavaScript
- 设计：玻璃拟态风格