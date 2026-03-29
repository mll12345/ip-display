from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    """返回主页"""
    return send_from_directory('.', 'index.html')

@app.route('/api/ip')
def get_client_ip():
    """获取客户端的公网IP地址"""
    # 尝试从各种HTTP头中获取真实IP（处理代理、CDN等场景）
    ip = None
    
    # 检查可能的代理头
    headers_to_check = [
        'X-Forwarded-For',
        'X-Real-IP',
        'CF-Connecting-IP',
        'X-Client-IP',
        'HTTP_X_FORWARDED_FOR',
        'HTTP_X_REAL_IP',
    ]
    
    for header in headers_to_check:
        if header in request.headers:
            ip = request.headers[header].split(',')[0].strip()
            break
    
    # 如果没有找到代理头，使用直接连接的IP
    if not ip:
        ip = request.remote_addr
    
    return jsonify({
        'ip': ip,
        'success': True
    })

if __name__ == '__main__':
    # 生产环境建议使用 gunicorn 或 uWSGI
    # 开发环境使用 Flask 内置服务器
    print("服务器启动中...")
    print("访问地址: http://127.0.0.1:5000")
    print("按 Ctrl+C 停止服务器")
    app.run(host='0.0.0.0', port=5000, debug=True)