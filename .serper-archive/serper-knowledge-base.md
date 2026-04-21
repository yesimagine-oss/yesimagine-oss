# Serper.dev 完整知识库

**创建时间:** 2026-03-21  
**最后更新:** 2026-03-21 12:45  
**状态:** ✅ 完整  

---

## 📊 概述

**Serper.dev 是什么:**
- 世界最快、最便宜的 Google Search API
- 1-2 秒返回 Google 搜索结果
- 适合 AI 应用、SEO 分析、金融项目等

**核心优势:**
- ⚡ **速度快** - 1-2 秒返回结果
- 💰 **价格低** - 比竞品便宜 10 倍
- 🎯 **实时性** - 实时搜索结果
- 🌍 **全球覆盖** - 支持自定义地理位置

---

## 🔑 账户信息

| 项目 | 信息 |
|------|------|
| **网站** | https://serper.dev |
| **邮箱** | red@unvw.com |
| **密码** | red753951 |
| **API Key** | `01529847d4aa3cf47b86ca87d28519110db06390` |
| **免费额度** | 2,500 次查询（注册即送） |
| **配置状态** | ✅ 已配置并测试通过 |
| **配置文件** | `/home/admin/.openclaw/workspace/.env.serper` |

---

## 🎯 10 种 API 端点

| 端点 | 功能 | 命令 | 用途 |
|------|------|------|------|
| `/search` | Google 网页搜索 | `search` | 通用搜索、资料收集 |
| `/images` | Google 图片搜索 | `images` | 找灵感图、参考素材 |
| `/news` | Google 新闻搜索 | `news` | 追踪热点、行业动态 |
| `/maps` | Google 地图搜索 | `maps` | 找场地、地点信息 |
| `/places` | Google 地点搜索 | `places` | 找商家、机构信息 |
| `/videos` | Google 视频搜索 | `videos` | 找视频、教程 |
| `/shopping` | Google 购物搜索 | `shopping` | 比价、产品调研 |
| `/scholar` | Google 学术搜索 | `scholar` | 学术论文、深度研究 |
| `/patents` | Google 专利搜索 | `patents` | 专利检索、技术创新 |
| `/autocomplete` | Google 搜索建议 | `autocomplete` | 发现相关话题 |

---

## 📝 API 使用示例

### 基础搜索

```bash
# Web 搜索
curl --request POST \
  --url https://google.serper.dev/search \
  --header 'X-API-KEY: 01529847d4aa3cf47b86ca87d28519110db06390' \
  --header 'Content-Type: application/json' \
  --data '{"q": "AI agent"}'
```

### 带参数搜索

```bash
# 指定国家、语言、页码
curl --request POST \
  --url https://google.serper.dev/search \
  --header 'X-API-KEY: 01529847d4aa3cf47b86ca87d28519110db06390' \
  --header 'Content-Type: application/json' \
  --data '{
    "q": "AI agent",
    "gl": "us",
    "hl": "en",
    "page": 1,
    "num": 10
  }'
```

### 新闻搜索（带时间范围）

```bash
# 最近 7 天的新闻
curl --request POST \
  --url https://google.serper.dev/news \
  --header 'X-API-KEY: 01529847d4aa3cf47b86ca87d28519110db06390' \
  --header 'Content-Type: application/json' \
  --data '{
    "q": "artificial intelligence",
    "tbs": "qdr:w"
  }'
```

### 地点搜索（带地理位置）

```bash
# 搜索旧金山的咖啡馆
curl --request POST \
  --url https://google.serper.dev/places \
  --header 'X-API-KEY: 01529847d4aa3cf47b86ca87d28519110db06390' \
  --header 'Content-Type: application/json' \
  --data '{
    "q": "coffee shops",
    "location": "San Francisco, CA, USA"
  }'
```

---

## 🔧 常用参数

### 通用参数

| 参数 | 说明 | 示例 | 默认值 |
|------|------|------|--------|
| `q` | 搜索关键词 | `"q": "AI agent"` | 必填 |
| `gl` | 国家代码 | `"gl": "us"` | `us` |
| `hl` | 语言代码 | `"hl": "en"` | `en` |
| `page` | 页码 | `"page": 1` | `1` |
| `num` | 结果数量 | `"num": 10` | `10` |

### 时间范围参数 (`tbs`)

| 参数 | 说明 | 示例 |
|------|------|------|
| `qdr:h` | 最近 1 小时 | `"tbs": "qdr:h"` |
| `qdr:d` | 最近 1 天 | `"tbs": "qdr:d"` |
| `qdr:w` | 最近 1 周 | `"tbs": "qdr:w"` |
| `qdr:m` | 最近 1 月 | `"tbs": "qdr:m"` |
| `qdr:y` | 最近 1 年 | `"tbs": "qdr:y"` |

### 地理位置参数

```json
{
  "location": "New York, USA"
}
```

支持：
- 城市：`"Beijing, China"`
- 州/省：`"California, USA"`
- 国家：`"United States"`
- 邮编：`"90210, USA"`

---

## 💰 定价方案

| 方案 | 价格 | 额度 | 单价 | QPS | 有效期 |
|------|------|------|------|-----|--------|
| **免费** | $0 | 2,500 次 | $0 | 5 | 永久 |
| **Starter** | $50 | 50k | $1.00/1k | 50 | 6 个月 |
| **Standard** | $375 | 500k | $0.75/1k | 100 | 6 个月 |
| **Scale** | $1,250 | 2.5M | $0.50/1k | 200 | 6 个月 |
| **Ultimate** | $3,750 | 12.5M | $0.30/1k | 300 | 6 个月 |

**特点:**
- ✅ 无月费，按需购买
- ✅ 额度 6 个月有效
- ✅ 比竞品便宜 10 倍

---

## 📊 响应格式

### Web 搜索响应

```json
{
  "searchParameters": {
    "q": "AI agent",
    "gl": "us",
    "hl": "en",
    "page": 1,
    "type": "search"
  },
  "knowledgeGraph": {
    "title": "AI agent",
    "type": "Topic",
    "description": "...",
    "descriptionSource": "Wikipedia",
    "descriptionLink": "https://..."
  },
  "organic": [
    {
      "title": "...",
      "link": "...",
      "snippet": "...",
      "position": 1,
      "sitelinks": [...]
    }
  ],
  "peopleAlsoAsk": [
    {
      "question": "...",
      "snippet": "...",
      "title": "...",
      "link": "..."
    }
  ],
  "relatedSearches": [
    {"query": "..."}
  ]
}
```

### 新闻搜索响应

```json
{
  "news": [
    {
      "title": "...",
      "link": "...",
      "snippet": "...",
      "date": "2 days ago",
      "source": "TechCrunch"
    }
  ]
}
```

### 地点搜索响应

```json
{
  "places": [
    {
      "title": "...",
      "address": "...",
      "latitude": 37.7749,
      "longitude": -122.4194,
      "rating": 4.5,
      "reviews": 123
    }
  ]
}
```

---

## 🚀 Python 集成

### 基础用法

```python
import requests
import json

def serper_search(query, endpoint="search", **params):
    """
    Serper API 搜索
    
    Args:
        query: 搜索关键词
        endpoint: API 端点 (search, images, news, etc.)
        **params: 其他参数 (gl, hl, location, etc.)
    
    Returns:
        dict: 搜索结果
    """
    url = f"https://google.serper.dev/{endpoint}"
    
    headers = {
        'X-API-KEY': '01529847d4aa3cf47b86ca87d28519110db06390',
        'Content-Type': 'application/json'
    }
    
    payload = {"q": query, **params}
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    return response.json()

# 使用示例
results = serper_search("AI agent")
print(json.dumps(results, indent=2))
```

### 新闻搜索（带时间过滤）

```python
def search_news(query, days=7):
    """搜索最近 N 天的新闻"""
    tbs_map = {
        1: "qdr:d",
        7: "qdr:w",
        30: "qdr:m",
        365: "qdr:y"
    }
    
    tbs = tbs_map.get(days, "qdr:w")
    
    results = serper_search(query, endpoint="news", tbs=tbs)
    return results.get("news", [])

# 使用
news = search_news("artificial intelligence", days=7)
for item in news[:5]:
    print(f"{item['date']}: {item['title']}")
```

### 地点搜索

```python
def search_places(query, location):
    """搜索某地点的商家/机构"""
    results = serper_search(query, endpoint="places", location=location)
    return results.get("places", [])

# 使用
cafes = search_places("coffee shops", "San Francisco, CA")
for cafe in cafes[:5]:
    print(f"{cafe['title']} - {cafe.get('rating', 'N/A')}⭐")
```

---

## 🔗 框架集成

### LangChain 集成

```python
from langchain.utilities import SerperAPIWrapper

search = SerperAPIWrapper(
    serper_api_key="01529847d4aa3cf47b86ca87d28519110db06390"
)

# 使用
result = search.run("EvoMap AI agent")
print(result)
```

### CrewAI 集成

```python
from crewai_tools import SerperDevTool

search_tool = SerperDevTool(
    serper_api_key="01529847d4aa3cf47b86ca87d28519110db06390"
)

# 在 Agent 中使用
result = search_tool.run(query="AI agent platform")
```

### Haystack 集成

```python
from haystack.components.websearch import SerperWebSearch

search = SerperWebSearch(api_key="01529847d4aa3cf47b86ca87d28519110db06390")

# 使用
documents = search.run(query="AI agent")
```

---

## 💡 使用场景

### 场景 1: 纪录片题材调研

```python
def research_documentary_topic(topic):
    """调研纪录片题材"""
    # 搜索相关作品
    works = serper_search(f"{topic} documentary award winning")
    
    # 搜索最新动态
    news = serper_search(f"{topic} documentary 2026", endpoint="news")
    
    # 搜索相关人物
    people = serper_search(f"{topic} documentary filmmaker")
    
    return {
        "works": works.get("organic", [])[:10],
        "news": news.get("news", [])[:5],
        "people": people.get("organic", [])[:5]
    }

# 使用
research = research_documentary_topic("western china")
```

### 场景 2: 展览场地调研

```python
def find_venues(city, venue_type="art space"):
    """找展览场地"""
    places = serper_search(
        venue_type,
        endpoint="places",
        location=f"{city}, China"
    )
    return places.get("places", [])

# 使用
venues = find_venues("Jinan", "art gallery")
for venue in venues:
    print(f"{venue['title']} - {venue.get('address', 'N/A')}")
```

### 场景 3: 行业动态监控

```python
def monitor_industry(keywords):
    """监控行业动态"""
    from datetime import datetime
    
    results = {}
    for keyword in keywords:
        news = serper_search(keyword, endpoint="news", tbs="qdr:w")
        results[keyword] = news.get("news", [])[:5]
    
    # 生成报告
    report = f"## 行业周报 - {datetime.now().strftime('%Y-%m-%d')}\n\n"
    for keyword, items in results.items():
        report += f"### {keyword}\n\n"
        for item in items:
            report += f"- [{item['title']}]({item['link']}) ({item.get('date', 'N/A')})\n"
        report += "\n"
    
    return report

# 使用
keywords = ["AI agent", "documentary film", "art exhibition"]
report = monitor_industry(keywords)
print(report)
```

### 场景 4: 技术问题解决

```python
def solve_technical_problem(problem):
    """搜索技术问题的解决方案"""
    results = serper_search(f"{problem} solution stackoverflow")
    
    # 提取最相关的结果
    solutions = []
    for item in results.get("organic", [])[:5]:
        solutions.append({
            "title": item["title"],
            "link": item["link"],
            "snippet": item.get("snippet", "")
        })
    
    return solutions

# 使用
solutions = solve_technical_problem("Feishu API permission error")
for sol in solutions:
    print(f"{sol['title']}\n{sol['link']}\n")
```

---

## ⚠️ 注意事项

### 额度管理

| 项目 | 说明 |
|------|------|
| **免费额度** | 2,500 次（注册即送，永久有效） |
| **额度消耗** | 每次 API 调用扣除 1 次 |
| **额度查询** | 登录 Dashboard 查看剩余额度 |
| **超额处理** | API 返回 402 错误，需购买额度 |

### 请求限制

| 方案 | QPS (每秒查询) |
|------|---------------|
| 免费 | 5 |
| Starter | 50 |
| Standard | 100 |
| Scale | 200 |
| Ultimate | 300 |

### 最佳实践

1. **缓存结果** - 相同查询缓存 24 小时
2. **批量查询** - 合并相似查询减少请求
3. **错误处理** - 处理 429 (限流)、402 (超额) 错误
4. **监控使用** - 定期检查额度使用情况

---

## 🔍 错误处理

```python
import requests
from requests.exceptions import RequestException

def safe_serper_search(query, **params):
    """带错误处理的搜索"""
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': '01529847d4aa3cf47b86ca87d28519110db06390',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, json={"q": query, **params}, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 402:
            return {"error": "额度不足，请充值"}
        elif response.status_code == 429:
            return {"error": "请求频率超限，请稍后重试"}
        else:
            return {"error": f"HTTP 错误：{e}"}
    
    except RequestException as e:
        return {"error": f"网络错误：{e}"}

# 使用
result = safe_serper_search("test")
if "error" in result:
    print(f"搜索失败：{result['error']}")
else:
    print("搜索成功")
```

---

## 📚 相关资源

| 资源 | 链接 |
|------|------|
| **官方网站** | https://serper.dev |
| **Dashboard** | https://serper.dev/dashboard |
| **Playground** | https://serper.dev/playground |
| **API 文档** | https://serper.dev/docs (需登录) |
| **状态页面** | https://status.serper.dev |
| **Twitter** | https://twitter.com/serperdev |
| **Medium** | https://medium.com/@serper |

---

## 🎯 快速开始清单

- [x] **注册账户** - 已完成
- [x] **获取 API Key** - 已完成
- [x] **配置环境变量** - 已完成
- [x] **测试 API 连接** - 已完成
- [ ] **熟悉 10 种端点** - 本文档已涵盖
- [ ] **集成到 OpenClaw** - 已配置
- [ ] **实际项目应用** - 随时开始

---

## 📝 更新日志

| 日期 | 更新内容 |
|------|---------|
| 2026-03-21 | 创建完整知识库，包含 API 文档、使用示例、集成指南 |

---

**知识库创建完成！现在您可以随时使用 Serper API 了！** 🎉

**快速使用:**
```bash
# 测试搜索
uv run /home/admin/.openclaw/workspace/skills/serper/scripts/serper.py search "AI agent"
```
