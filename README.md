# MiMo Meter

本地 API 用量监控工具，专为小米 MiMo Token Plan 设计。

**一句话：下载运行，填入 API Key，改代码里的 API 地址，完事。**

---

## 快速开始

### Windows 用户

1. 下载 [MimoMeter.exe](https://github.com/Dragon-01-you/MimoMeter/releases/latest)
2. 双击运行，浏览器自动打开
3. 点击「设置 API」，填入你的 API Key
4. 点击「测试连接」验证
5. 修改代码里的 API 地址

### macOS / Linux 用户

```bash
git clone https://github.com/Dragon-01-you/MimoMeter.git
cd MimoMeter
pip install aiohttp
python -m src
```

---

## API 地址

| 格式 | 地址 |
|------|------|
| OpenAI | `http://127.0.0.1:8080/v1` |
| Anthropic | `http://127.0.0.1:8080/anthropic` |
| 仪表盘 | `http://127.0.0.1:8081` |

---

## AI 配置方法（推荐）

不想手动配置？把下面的提示词发给 AI，让它帮你配好：

### 给 Cursor 的提示词

```
我有一个本地 API 代理 MiMo Meter，运行在 http://127.0.0.1:8080

请帮我配置 Cursor，把 OpenAI Base URL 改成:
http://127.0.0.1:8080/v1

API Key 保持不变。
```

### 给 Claude Code 的提示词

```
我有一个本地 API 代理 MiMo Meter，运行在 http://127.0.0.1:8080

请帮我配置 Claude Code，让它通过本地代理访问 MiMo API：

方法一：设置环境变量
export ANTHROPIC_BASE_URL=http://127.0.0.1:8080/anthropic

方法二：修改 ~/.claude/settings.json
{
  "apiBaseUrl": "http://127.0.0.1:8080/anthropic"
}
```

### 给任意 AI 的通用提示词

```
我有一个本地 API 代理 MiMo Meter，运行在 http://127.0.0.1:8080

请帮我配置 [工具名称]，让它通过这个代理访问 MiMo API：

- OpenAI 格式: http://127.0.0.1:8080/v1
- Anthropic 格式: http://127.0.0.1:8080/anthropic

我的 API Key 是: [填入你的 Key]

请帮我修改配置文件，让所有 API 请求都走本地代理。
```

---

## 代码配置

### Python (openai 库)

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8080/v1",
    api_key="你的 API Key"
)

response = client.chat.completions.create(
    model="mimo-v2.5-pro",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

### Python (anthropic 库)

```python
from anthropic import Anthropic

client = Anthropic(
    base_url="http://127.0.0.1:8080/anthropic",
    api_key="你的 API Key"
)

response = client.messages.create(
    model="mimo-v2.5-pro",
    max_tokens=100,
    messages=[{"role": "user", "content": "你好"}]
)
print(response.content[0].text)
```

### Cursor

设置 → OpenAI Base URL → `http://127.0.0.1:8080/v1`

### VS Code

设置 → 插件 API URL → `http://127.0.0.1:8080/v1`

### Claude Code

```bash
export ANTHROPIC_BASE_URL=http://127.0.0.1:8080/anthropic
```

### Claude Desktop

设置 → Anthropic Base URL → `http://127.0.0.1:8080/anthropic`

---

## 功能

- 实时用量监控（仪表盘自动刷新）
- 支持 OpenAI 和 Anthropic 两种格式
- 按模型统计用量
- 7 天趋势图表
- 导出 CSV / JSON
- 本地 SQLite 存储，数据不上传

---

## 获取 API Key

1. 打开 https://token-plan-cn.xiaomimimo.com
2. 登录小米账号
3. 在控制台找到 API Key
4. 复制使用

---

## 技术栈

- Python 3.11+
- aiohttp
- SQLite
- Chart.js
- PyInstaller

---

## 许可证

MIT License
