import json
import time
import aiohttp
from aiohttp import web

# 支持 PyInstaller 打包
try:
    from .db import record_usage
    from .logger import log_request, log_error
except ImportError:
    from db import record_usage
    from logger import log_request, log_error

# MiMo Token Plan API 地址
TARGET_API = "https://token-plan-cn.xiaomimimo.com"

def parse_usage(data, path):
    """解析 usage 信息，支持 OpenAI 和 Anthropic 格式"""
    usage = data.get('usage', {})
    model = data.get('model', 'unknown')

    # Anthropic 格式: /anthropic/v1/messages（必须先检查，因为路径也包含 /v1/）
    if '/anthropic/' in path:
        return {
            'model': model,
            'prompt': usage.get('input_tokens', 0),
            'completion': usage.get('output_tokens', 0),
            'total': usage.get('input_tokens', 0) + usage.get('output_tokens', 0)
        }

    # OpenAI 格式: /v1/chat/completions
    if '/v1/' in path:
        return {
            'model': model,
            'prompt': usage.get('prompt_tokens', 0),
            'completion': usage.get('completion_tokens', 0),
            'total': usage.get('total_tokens', 0)
        }

    # 通用格式
    return {
        'model': model,
        'prompt': usage.get('prompt_tokens', 0) or usage.get('input_tokens', 0),
        'completion': usage.get('completion_tokens', 0) or usage.get('output_tokens', 0),
        'total': usage.get('total_tokens', 0) or (usage.get('input_tokens', 0) + usage.get('output_tokens', 0))
    }

async def handle_request(request):
    """透明代理：转发请求到官方 API，同时记录用量"""
    start_time = time.time()
    path = request.path

    # 构建目标 URL
    target_url = f"{TARGET_API}{request.path_qs}"

    # 复制 headers，去掉 Host
    headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}

    # 读取请求体
    body = await request.read()

    # 检查是否是流式请求
    is_stream = False
    try:
        body_json = json.loads(body)
        is_stream = body_json.get('stream', False)
    except:
        pass

    # 转发到官方 API
    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=body,
                ssl=True,
                timeout=aiohttp.ClientTimeout(total=300)
            ) as resp:

                status = resp.status

                # 流式响应处理
                if is_stream and status == 200:
                    response = web.StreamResponse(
                        status=status,
                        headers={
                            'Content-Type': 'text/event-stream',
                            'Cache-Control': 'no-cache',
                            'Connection': 'keep-alive',
                        }
                    )
                    await response.prepare(request)

                    # 收集流式数据以解析 usage
                    collected_data = None
                    model = 'unknown'

                    async for chunk in resp.content.iter_any():
                        await response.write(chunk)
                        chunk_str = chunk.decode('utf-8', errors='ignore')

                        # 解析 SSE 数据
                        for line in chunk_str.split('\n'):
                            if line.startswith('data: '):
                                data_str = line[6:].strip()
                                if data_str == '[DONE]':
                                    continue
                                try:
                                    data = json.loads(data_str)
                                    if 'model' in data:
                                        model = data['model']
                                    # 收集 usage 信息
                                    if 'usage' in data:
                                        collected_data = data
                                except:
                                    pass

                    # 解析 usage
                    if collected_data:
                        u = parse_usage(collected_data, path)
                        record_usage(
                            model=u['model'],
                            prompt=u['prompt'],
                            completion=u['completion'],
                            total=u['total'],
                            status="success"
                        )
                        duration_ms = (time.time() - start_time) * 1000
                        log_request(request.method, path, 200, duration_ms, u)

                    await response.write_eof()
                    return response

                # 非流式响应处理
                response_body = await resp.read()

                # 解析 usage
                if status == 200 and 'application/json' in resp.headers.get('Content-Type', ''):
                    try:
                        data = json.loads(response_body)
                        if 'usage' in data:
                            u = parse_usage(data, path)
                            record_usage(
                                model=u['model'],
                                prompt=u['prompt'],
                                completion=u['completion'],
                                total=u['total'],
                                status="success"
                            )
                            duration_ms = (time.time() - start_time) * 1000
                            log_request(request.method, path, status, duration_ms, u)
                    except Exception as e:
                        log_error("解析失败", e)

                # 原样返回给客户端
                return web.Response(
                    body=response_body,
                    status=status,
                    headers={k: v for k, v in resp.headers.items()
                            if k.lower() not in ('content-encoding', 'transfer-encoding')}
                )
        except Exception as e:
            log_error("代理错误", e)
            return web.Response(text=f"代理错误: {str(e)}", status=502)

app = web.Application()
app.router.add_route('*', '/{path:.*}', handle_request)
