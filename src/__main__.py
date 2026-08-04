import asyncio
import sys
import os
from aiohttp import web

# 添加当前目录到 Python 路径
if getattr(sys, 'frozen', False):
    # PyInstaller 打包后的路径
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, base_dir)

# 导入模块
try:
    from proxy import app as proxy_app
    from dashboard import dashboard_app
    from db import init_db
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Base dir: {base_dir}")
    print(f"sys.path: {sys.path}")
    sys.exit(1)

async def main():
    """主入口：启动代理服务器和仪表盘"""
    # 初始化数据库
    init_db()
    print("MiMo Meter starting...")

    # 启动代理服务器 (8080)
    proxy_runner = web.AppRunner(proxy_app)
    await proxy_runner.setup()
    await web.TCPSite(proxy_runner, '127.0.0.1', 8080).start()
    print("Proxy: http://127.0.0.1:8080")

    # 启动仪表盘 (8081)
    dashboard_runner = web.AppRunner(dashboard_app)
    await dashboard_runner.setup()
    await web.TCPSite(dashboard_runner, '127.0.0.1', 8081).start()
    print("Dashboard: http://127.0.0.1:8081")

    print("\n" + "="*50)
    print("Usage:")
    print("  OpenAI:    http://127.0.0.1:8080/v1")
    print("  Anthropic: http://127.0.0.1:8080/anthropic")
    print("  Dashboard: http://127.0.0.1:8081")
    print("="*50 + "\n")

    # 自动打开浏览器
    import webbrowser
    webbrowser.open('http://127.0.0.1:8081')

    # 保持运行
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    asyncio.run(main())
