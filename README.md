# MiMo Meter

本地 API 用量监控工具，专为小米 MiMo Token Plan 设计。

---

## 一句话配置（推荐）

把下面这段话发给任意 AI（Cursor、Claude Code、ChatGPT 等），它会帮你完成所有步骤：

```
帮我配置 MiMo Meter 本地 API 代理：

1. 从这里下载：https://github.com/Dragon-01-you/MimoMeter/releases/latest
2. 下载 MimoMeter.exe，双击运行
3. 浏览器会自动打开，在「设置 API」页面填入我的 API Key
4. 把我代码里的 API 地址改成：
   - OpenAI 格式: http://127.0.0.1:8080/v1
   - Anthropic 格式: http://127.0.0.1:8080/anthropic

我的 API Key 是: [在这里填入你的 Key]

请帮我完成以上所有步骤。
```

**用户只需要提供 API Key，AI 会自动完成下载、运行、配置。**

---

## AI 完整配置提示词

如果你希望 AI 帮你完成所有操作，复制以下内容：

```
请帮我完成 MiMo Meter 的全部配置：

第一步：下载安装
- 从 https://github.com/Dragon-01-you/MimoMeter/releases/latest 下载 MimoMeter.exe
- 双击运行，浏览器会自动打开 http://127.0.0.1:8081

第二步：配置 API Key
- 在仪表盘页面点击「设置 API」
- 填入 API Key: [你的 Key]
- 点击「测试连接」验证
- 点击「保存配置」

第三步：修改我的代码
- 把所有 API 调用的地址改成:
  - OpenAI 格式: http://127.0.0.1:8080/v1
  - Anthropic 格式: http://127.0.0.1:8080/anthropic
- API Key 保持不变

请帮我完成以上所有步骤，并告诉我改了哪些文件。
```

---

## 分步配置提示词

如果你只需要 AI 帮你配置某个工具：

### 配置 Cursor

```
帮我配置 Cursor 使用 MiMo Meter 代理：
1. 下载运行 MimoMeter.exe: https://github.com/Dragon-01-you/MimoMeter/releases/latest
2. 在 Cursor 设置中，把 OpenAI Base URL 改成: http://127.0.0.1:8080/v1
3. API Key 保持不变
```

### 配置 Claude Code

```
帮我配置 Claude Code 使用 MiMo Meter 代理：
1. 下载运行 MimoMeter.exe: https://github.com/Dragon-01-you/MimoMeter/releases/latest
2. 设置环境变量: export ANTHROPIC_BASE_URL=http://127.0.0.1:8080/anthropic
3. 或者修改 ~/.claude/settings.json 添加: {"apiBaseUrl": "http://127.0.0.1:8080/anthropic"}
```

### 配置 Python 项目

```
帮我配置 Python 项目使用 MiMo Meter 代理：
1. 下载运行 MimoMeter.exe: https://github.com/Dragon-01-you/MimoMeter/releases/latest
2. 修改代码中的 OpenAI 客户端：
   client = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="我的Key")
3. 或者 Anthropic 客户端：
   client = Anthropic(base_url="http://127.0.0.1:8080/anthropic", api_key="我的Key")
```

### 配置 VS Code

```
帮我配置 VS Code 使用 MiMo Meter 代理：
1. 下载运行 MimoMeter.exe: https://github.com/Dragon-01-you/MimoMeter/releases/latest
2. 在 VS Code 设置中找到 AI 插件的 API 配置
3. 把 Base URL 改成: http://127.0.0.1:8080/v1
4. API Key 保持不变
```

---

## 获取 API Key

1. 打开 https://token-plan-cn.xiaomimimo.com
2. 登录小米账号
3. 在控制台找到 API Key
4. 复制使用

---

## 手动配置

### Windows 用户

1. 下载 [MimoMeter.exe](https://github.com/Dragon-01-you/MimoMeter/releases/latest)
2. 双击运行
3. 浏览器自动打开，点击「设置 API」
4. 填入 API Key，测试连接
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

## 代码示例

### Python (openai)

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

### Python (anthropic)

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

---

## 功能

- 实时用量监控
- 支持 OpenAI 和 Anthropic 格式
- 按模型统计
- 7 天趋势图表
- 导出 CSV / JSON
- 本地存储，数据不上传

---

## 许可证

MIT License
