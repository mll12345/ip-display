from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import requests
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    """返回主页"""
    return send_from_directory('.', 'index.html')

@app.route('/bg.jpg')
def bg_image():
    """返回背景图片"""
    return send_from_directory('.', 'bg.jpg')

@app.route('/api/ip')
def get_client_ip():
    """获取客户端的公网IP地址并记录到文件"""
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
    
    # 记录IP地址到文件
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {ip}\n"
        
        # 追加模式写入文件
        with open('IP.txt', 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(f"记录访问: {ip} 于 {timestamp}")
    except Exception as e:
        print(f"记录IP失败: {e}")
    
    # 调用 ip-api.com API 获取IP详细信息
    try:
        ipapi_url = f"http://ip-api.com/json/{ip}?lang=zh-CN"
        response = requests.get(ipapi_url, timeout=5)
        
        if response.status_code == 200:
            location_info = response.json()
            # 追加写入 dizhi.txt
            with open('dizhi.txt', 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} - {ip} - {location_info}\n")
            print(f"记录地址信息: {ip} - {location_info}")
        else:
            print(f"获取地址信息失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"获取地址信息异常: {e}")
    
    # 调用 ip-api.com API 获取IP详细信息
    location_info = None
    try:
        ipapi_url = f"http://ip-api.com/json/{ip}?lang=zh-CN"
        response = requests.get(ipapi_url, timeout=5)
        
        if response.status_code == 200:
            location_info = response.json()
            # 追加写入 dizhi.txt
            with open('dizhi.txt', 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} - {ip} - {location_info}\n")
            print(f"记录地址信息: {ip} - {location_info}")
        else:
            print(f"获取地址信息失败: HTTP {response.status_code}")
    except Exception as e:
        print(f"获取地址信息异常: {e}")
    
    return jsonify({
        'ip': ip,
        'success': True,
        'location': location_info
    })

if __name__ == '__main__':
    # 生产环境建议使用 gunicorn 或 uWSGI
    # 开发环境使用 Flask 内置服务器
    # 注意：使用80端口需要管理员权限
    print("服务器启动中...")
    print("访问地址: http://127.0.0.1")
    print("按 Ctrl+C 停止服务器")
    app.run(host='0.0.0.0', port=80, debug=True)