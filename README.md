# MimoMeter（米莫电表）

本地 API 用量监控工具，专为小米 MiMo Token Plan 设计。

## 功能特性

- ✅ 零代码侵入：只需改 API Base URL
- ✅ 数据完全本地：SQLite 存储，隐私安全
- ✅ 单文件运行：PyInstaller 打包，无需安装 Python
- ✅ 实时可视化仪表盘：自动刷新，一目了然
- ✅ 系统托盘运行：后台静默运行，不打扰工作
- ✅ 支持 OpenAI 和 Anthropic 两种格式

## 快速开始

### 方式一：直接运行（需要 Python 环境）

```bash
# 安装依赖
pip install -r requirements.txt

# 运行
python -m src
```

### 方式二：打包成可执行文件

```bash
# 安装打包工具
pip install pyinstaller

# 一键打包
python build.py

# 生成的文件在 dist/MimoMeter.exe
```

## 使用方法

1. 双击运行 MimoMeter.exe
2. 自动弹出浏览器仪表盘
3. 将你的 API Base URL 改为 `http://127.0.0.1:8080`
4. 正常调用 API，用量会自动记录

### OpenAI 格式（Python）

```python
from openai import OpenAI

# 原来
# client = OpenAI(base_url="https://token-plan-cn.xiaomimimo.com/v1", api_key="...")

# 现在（只改这一行）
client = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="...")

response = client.chat.completions.create(
    model="mimo-claw",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Anthropic 格式（Python）

```python
from anthropic import Anthropic

# 原来
# client = Anthropic(base_url="https://token-plan-cn.xiaomimimo.com/anthropic", api_key="...")

# 现在（只改这一行）
client = Anthropic(base_url="http://127.0.0.1:8080/anthropic", api_key="...")

response = client.messages.create(
    model="mimo-claw",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Cursor/VS Code

在设置里找到 OpenAI Base URL，改成 `http://127.0.0.1:8080/v1`

### Claude Code / Claude Desktop

在设置里找到 Anthropic Base URL，改成 `http://127.0.0.1:8080/anthropic`

## 仪表盘功能

- 今日 Token 消耗（Input/Output 分开显示）
- 累计 Token 消耗
- 平均每次调用消耗
- 近 7 天用量趋势图
- 按模型分布统计
- 最近调用记录
- 数据导出（CSV/JSON）

## 数据存储

数据存储在用户主目录下的 `.mimo-meter/usage.db` 文件中：

- Windows: `C:\Users\你的用户名\.mimo-meter\usage.db`
- macOS/Linux: `~/.mimo-meter/usage.db`

## GitHub Actions 自动构建

项目配置了 GitHub Actions，打 Tag 会自动构建 Windows 和 macOS 版本：

```bash
git tag v1.0.0
git push origin v1.0.0
```

会在 GitHub Releases 页面自动生成可下载的可执行文件。

## 技术栈

- Python 3.11+
- aiohttp：异步 HTTP 服务器
- SQLite：本地数据存储
- Chart.js：前端图表
- PyInstaller：打包成可执行文件
- pystray：系统托盘图标

## 许可证

MIT License
