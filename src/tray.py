import pystray
from PIL import Image, ImageDraw
import webbrowser
import threading

def create_image():
    """生成系统托盘图标"""
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), '#0f172a')
    dc = ImageDraw.Draw(image)
    # 画一个闪电图标
    dc.polygon([(32, 10), (20, 35), (30, 35), (25, 55), (45, 30), (35, 30)], fill='#38bdf8')
    return image

def run_tray():
    """运行系统托盘图标"""
    menu = pystray.Menu(
        pystray.MenuItem("打开仪表盘", lambda: webbrowser.open('http://127.0.0.1:8081')),
        pystray.MenuItem("退出", lambda: icon.stop())
    )
    icon = pystray.Icon("MimoMeter", create_image(), "MiMo Meter 运行中", menu)
    icon.run()
