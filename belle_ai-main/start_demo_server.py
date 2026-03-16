#!/usr/bin/env python3
"""简单的本地 HTTP 服务器，用于运行 demo.html

使用方法：
    python start_demo_server.py

然后在浏览器访问：
    http://127.0.0.1:8080/demo.html
"""
import http.server
import socketserver
import webbrowser
import os

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """自定义请求处理器，添加 CORS 头"""
    
    def end_headers(self):
        # 添加 CORS 头，允许跨域请求
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        """处理 OPTIONS 预检请求"""
        self.send_response(200)
        self.end_headers()

def main():
    """启动服务器"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        demo_url = f"http://127.0.0.1:{PORT}/demo.html"
        vision_demo_url = f"http://127.0.0.1:{PORT}/demo_vision_similar.html"
        print("=" * 60)
        print("🚀 Demo 服务器已启动！")
        print("=" * 60)
        print(f"📱 销售建议 Demo: {demo_url}")
        print(f"📱 拍照识图 Demo: {vision_demo_url}")
        print(f"🔧 API 后端: http://127.0.0.1:8000")
        print("=" * 60)
        print("按 Ctrl+C 停止服务器")
        print("=" * 60)
        
        # 自动打开浏览器（默认打开销售建议 Demo）
        try:
            webbrowser.open(demo_url)
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n服务器已停止")

if __name__ == "__main__":
    main()

