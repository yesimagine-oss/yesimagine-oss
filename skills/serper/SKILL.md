---
name: serper
description: Serper.dev Google Search API 集成技能。支持 10 种搜索类型：Web、图片、新闻、地图、地点、视频、购物、学术、专利、自动补全。
author: OpenClaw Workspace
version: 1.0.0
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["python3","curl"]},"config":{"env":{"SERPER_API_KEY":{"description":"Serper API Key","default":"01529847d4aa3cf47b86ca87d28519110db06390","required":true}}}}}
---

# Serper API 搜索技能

使用 Serper.dev API 执行 Google 搜索 - 支持 10 种搜索类型，快速、准确、结构化。

## 命令

### Web 搜索
```bash
uv run {baseDir}/scripts/serper.py search "query"              # 默认搜索
uv run {baseDir}/scripts/serper.py search "query" -n 20        # 20 个结果
uv run {baseDir}/scripts/serper.py search "query" --format json # JSON 输出
```

### 图片搜索
```bash
uv run {baseDir}/scripts/serper.py images "query"
uv run {baseDir}/scripts/serper.py images "AI robot" -n 10
```

### 新闻搜索
```bash
uv run {baseDir}/scripts/serper.py news "query"
uv run {baseDir}/scripts/serper.py news "AI technology" --time-range day
```

### 地图搜索
```bash
uv run {baseDir}/scripts/serper.py maps "coffee shops" --location "San Francisco, CA"
```

### 地点搜索
```bash
uv run {baseDir}/scripts/serper.py places "restaurants" --location "New York, USA"
```

### 视频搜索
```bash
uv run {baseDir}/scripts/serper.py videos "query"
```

### 购物搜索
```bash
uv run {baseDir}/scripts/serper.py shopping "laptop computer"
```

### 学术搜索
```bash
uv run {baseDir}/scripts/serper.py scholar "machine learning"
```

### 专利搜索
```bash
uv run {baseDir}/scripts/serper.py patents "artificial intelligence"
```

### 自动补全
```bash
uv run {baseDir}/scripts/serper.py autocomplete "artificial int"
```

## 高级选项

```bash
# 国家代码
uv run {baseDir}/scripts/serper.py search "query" --country us

# 语言代码
uv run {baseDir}/scripts/serper.py search "query" --language zh-CN

# 时间范围 (hour/day/week/month/year)
uv run {baseDir}/scripts/serper.py news "query" --time-range day

# 地理位置
uv run {baseDir}/scripts/serper.py maps "query" --location "Beijing, China"

# JSON 输出
uv run {baseDir}/scripts/serper.py search "query" --format json
```

## 配置

**必需:** 设置 `SERPER_API_KEY` 环境变量：

```bash
export SERPER_API_KEY=01529847d4aa3cf47b86ca87d28519110db06390
```

或在 Clawdbot 配置中：
```json
{
  "env": {
    "SERPER_API_KEY": "01529847d4aa3cf47b86ca87d28519110db06390"
  }
}
```

## 特性

- 🔍 **10 种搜索类型** - Web、图片、新闻、地图、地点、视频、购物、学术、专利、自动补全
- ⚡ **快速响应** - 1-2 秒返回结果
- 📊 **结构化数据** - JSON 格式，易于处理
- 🌍 **全球覆盖** - 支持多国语言和地区
- 🎯 **精准定位** - 支持地理位置定制

## API 端点

| 端点 | 命令 | 说明 |
|------|------|------|
| `/search` | `search` | Google 网页搜索 |
| `/images` | `images` | Google 图片搜索 |
| `/news` | `news` | Google 新闻搜索 |
| `/maps` | `maps` | Google 地图搜索 |
| `/places` | `places` | Google 地点搜索 |
| `/videos` | `videos` | Google 视频搜索 |
| `/shopping` | `shopping` | Google 购物搜索 |
| `/scholar` | `scholar` | Google 学术搜索 |
| `/patents` | `patents` | Google 专利搜索 |
| `/autocomplete` | `autocomplete` | Google 搜索建议 |

## 使用示例

### Python 集成
```python
import requests

def serper_search(query, endpoint="search"):
    url = f"https://google.serper.dev/{endpoint}"
    headers = {
        "X-API-KEY": "01529847d4aa3cf47b86ca87d28519110db06390",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json={"q": query}, headers=headers)
    return response.json()

# 使用
results = serper_search("AI agent")
```

### LangChain 集成
```python
from langchain.utilities import SerperAPIWrapper

search = SerperAPIWrapper(
    serper_api_key="01529847d4aa3cf47b86ca87d28519110db06390"
)
result = search.run("EvoMap AI agent")
```

### CrewAI 集成
```python
from crewai_tools import SerperDevTool

search_tool = SerperDevTool(
    serper_api_key="01529847d4aa3cf47b86ca87d28519110db06390"
)
result = search_tool.run(query="AI agent platform")
```

## 参考资源

| 资源 | 链接 |
|------|------|
| **官方文档** | https://serper.dev/docs |
| **Dashboard** | https://serper.dev/dashboard |
| **知识库** | `/home/admin/.openclaw/workspace/serper-knowledge-base/` |

---

**版本:** 1.0.0  
**创建日期:** 2026-03-15  
**状态:** ✅ 完成
