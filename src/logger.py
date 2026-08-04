import os
import logging
from datetime import datetime

# 日志目录
LOG_DIR = os.path.join(os.path.expanduser("~"), ".mimo-meter", "logs")

def setup_logger():
    """设置日志记录器"""
    os.makedirs(LOG_DIR, exist_ok=True)

    # 创建日志文件名（按日期）
    log_file = os.path.join(LOG_DIR, f"mimo-meter-{datetime.now().strftime('%Y-%m-%d')}.log")

    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger('mimo-meter')

logger = setup_logger()

def log_request(method, path, status, duration_ms, tokens=None):
    """记录请求日志"""
    token_info = ""
    if tokens:
        token_info = f" | tokens: {tokens.get('prompt', 0)}+{tokens.get('completion', 0)}={tokens.get('total', 0)}"

    logger.info(f"{method} {path} -> {status} ({duration_ms:.0f}ms{token_info})")

def log_error(msg, exc=None):
    """记录错误日志"""
    if exc:
        logger.error(f"{msg}: {exc}")
    else:
        logger.error(msg)
