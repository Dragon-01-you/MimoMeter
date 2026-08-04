from aiohttp import web
import os
import csv
import io

# 支持 PyInstaller 打包
try:
    from .db import get_stats, export_csv, export_json
except ImportError:
    from db import get_stats, export_csv, export_json

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

async def api_stats(request):
    return web.json_response(get_stats())

async def api_export_csv(request):
    rows = export_csv()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['timestamp', 'model', 'prompt_tokens', 'completion_tokens', 'total_tokens', 'status'])
    writer.writerows(rows)
    return web.Response(
        body=output.getvalue(),
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="mimo-meter-export.csv"'}
    )

async def api_export_json(request):
    data = export_json()
    return web.json_response(data)

async def index(request):
    html_path = os.path.join(STATIC_DIR, 'index.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            return web.Response(text=f.read(), content_type='text/html')
    return web.Response(text="Dashboard not found", status=404)

dashboard_app = web.Application()
dashboard_app.router.add_get('/api/stats', api_stats)
dashboard_app.router.add_get('/api/export/csv', api_export_csv)
dashboard_app.router.add_get('/api/export/json', api_export_json)
dashboard_app.router.add_get('/', index)
if os.path.exists(STATIC_DIR):
    dashboard_app.router.add_static('/static', STATIC_DIR)
