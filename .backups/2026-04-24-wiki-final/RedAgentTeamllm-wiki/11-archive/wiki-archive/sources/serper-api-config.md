---
category: source
created_at: '2026-04-14'
tags:
- source
- auto-generated
title: Serper Api Config
type: source
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# Serper.dev API Key 配置

**保存日期:** 2026-03-14  
**状态:** ✅ 已配置

---

## 🔑 API Key 信息

```bash
SERPER_API_KEY=01529847d4aa3cf47b86ca87d28519110db06390
```

---

## 📁 配置文件位置

### 方式 1: 环境变量文件（推荐）

**文件:** `/home/admin/.openclaw/workspace/.env.serper`

```bash
# Serper.dev API 配置
SERPER_API_KEY=01529847d4aa3cf47b86ca87d28519110db06390
SERPER_API_URL=https://google.serper.dev
```

### 方式 2: 全局环境变量

**添加到:** `~/.bashrc` 或 `~/.zshrc`

```bash
export SERPER_API_KEY=01529847d4aa3cf47b86ca87d28519110db06390
```

### 方式 3: 项目配置文件

**添加到:** `/home/admin/.openclaw/workspace/.env`

```bash
# Serper.dev
SERPER_API_KEY=01529847d4aa3cf47b86ca87d28519110db06390
```

---

## 🚀 快速开始

### 1. 测试 API 连接

**使用 curl 测试:**

```bash
curl --request POST \
  --url https://google.serper.dev/search \
  --header 'X-API-KEY: 01529847d4aa3cf47b86ca87d28519110db06390' \
  --header 'Content-Type: application/json' \
  --data '{
  "q": "EvoMap AI"
}'
```

**预期响应:**

```json
{
  "searchParameters": {
    "q": "EvoMap AI",
    "gl": "us",
    "hl": "en",
    "autocorrect": true,
    "page": 1,
    "type": "search"
  },
  "organic": [
    {
      "title": "...",
      "link": "...",
      "snippet": "..."
    }
  ]
}
```

### 2. Python 使用示例

```python
import requests

def serper_search(query):
    url = "https://google.serper.dev/search"
    
    payload = {"q": query}
    headers = {
        'X-API-KEY': '01529847d4aa3cf47b86ca87d28519110db06390',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# 使用示例
results = serper_search("EvoMap AI agent")
print(results)
```

### 3. Node.js 使用示例

```javascript
const axios = require('axios');

async function serperSearch(query) {
  const response = await axios.post(
    'https://google.serper.dev/search',
    { q: query },
    {
      headers: {
        'X-API-KEY': '01529847d4aa3cf47b86ca87d28519110db06390',
        'Content-Type': 'application/json'
      }
    }
  );
  
  return response.data;
}

// 使用示例
serperSearch('EvoMap AI agent').then(console.log);
```

---

## 📊 API 端点说明

| 端点 | 功能 | 请求方法 |
|------|------|---------|
| `/search` | Web 搜索 | POST |
| `/images` | 图片搜索 | POST |
| `/news` | 新闻搜索 | POST |
| `/places` | 地点搜索 | POST |
| `/scholar` | 学术搜索 | POST |

---

## 🔧 常用参数

### 通用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `q` | 搜索关键词 | `"q": "AI agent"` |
| `gl` | 国家代码 | `"gl": "us"` |
| `hl` | 语言代码 | `"hl": "en"` |
| `page` | 页码 | `"page": 1` |
| `num` | 结果数量 | `"num": 10` |

### 高级参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `tbs` | 时间过滤 | `"tbs": "qdr:y"` (最近 1 年) |
| `location` | 地理位置 | `"location": "New York, USA"` |
| `autocorrect` | 自动纠正 | `"autocorrect": true` |

---

## 💡 使用场景

### 场景 1: AI 助手搜索增强

```python
def ai_assistant_search(question):
    """为 AI 助手提供实时搜索能力"""
    results = serper_search(question)
    
    # 提取最有用的信息
    top_results = results.get('organic', [])[:5]
    
    # 格式化返回
    context = "\n".join([
        f"{r['title']}: {r['snippet']}"
        for r in top_results
    ])
    
    return context
```

### 场景 2: 竞品监控

```python
def monitor_competitors(competitors):
    """监控竞争对手动态"""
    for competitor in competitors:
        results = serper_search(f"{competitor} news")
        news = results.get('news', [])[:3]
        
        print(f"\n=== {competitor} 最新动态 ===")
        for item in news:
            print(f"- {item['title']} ({item['date']})")
```

### 场景 3: 市场调研

```python
def market_research(topic):
    """市场调研"""
    # Web 搜索
    web_results = serper_search(f"{topic} market trends")
    
    # 新闻搜索
    news_results = serper_search(f"{topic} news", endpoint='news')
    
    # 整理报告
    report = {
        'web_insights': web_results.get('organic', [])[:10],
        'news_updates': news_results.get('news', [])[:5]
    }
    
    return report
```

---

## ⚠️ 使用限制

| 项目 | 限制 |
|------|------|
| **免费额度** | 待确认（登录 dashboard 查看） |
| **请求频率** | 待确认 |
| **并发限制** | 待确认 |
| **数据缓存** | 搜索结果会缓存 |

**建议:**
- 登录 dashboard 查看具体额度
- 添加请求频率控制
- 实现结果缓存避免重复请求

---

## 🔒 安全最佳实践

### ✅ 推荐做法

```bash
# 1. 使用环境变量
export SERPER_API_KEY=01529847d4aa3cf47b86ca87d28519110db06390

# 2. 在代码中读取
import os
api_key = os.getenv('SERPER_API_KEY')

# 3. 添加到 .gitignore
echo ".env" >> .gitignore
```

### ❌ 避免做法

```python
# ❌ 不要硬编码在代码中
API_KEY = "01529847d4aa3cf47b86ca87d28519110db06390"

# ❌ 不要提交到 Git
git add .env  # 错误！

# ❌ 不要在公开场合分享
print(f"My API key: {API_KEY}")  # 错误！
```

---

## 📝 下一步

### 立即可做

1. **测试 API 连接**
   ```bash
   curl --request POST \
     --url https://google.serper.dev/search \
     --header 'X-API-KEY: 01529847d4aa3cf47b86ca87d28519110db06390' \
     --header 'Content-Type: application/json' \
     --data '{"q": "test"}'
   ```

2. **查看使用额度**
   - 登录：https://serper.dev
   - 查看 Dashboard
   - 确认剩余额度

3. **编写测试脚本**
   - 创建测试文件
   - 验证各个端点
   - 记录响应格式

### 后续工作

1. **集成到 OpenClaw**
   - 创建搜索技能
   - 添加搜索命令
   - 测试使用

2. **创建知识库**
   - 整理 API 文档
   - 编写使用示例
   - 创建最佳实践

---

## 📁 相关文件

| 文件 | 位置 |
|------|------|
| **API Key 配置** | `/home/admin/.openclaw/workspace/.env.serper` |
| **账户信息** | `/home/admin/.openclaw/workspace/memory/serper-account.md` |
| **使用示例** | `/home/admin/.openclaw/workspace/serper-examples/` (待创建) |

---

**API Key 已保存并配置完成!** ✅

**测试命令:**
```bash
curl --request POST \
  --url https://google.serper.dev/search \
  --header 'X-API-KEY: 01529847d4aa3cf47b86ca87d28519110db06390' \
  --header 'Content-Type: application/json' \
  --data '{"q": "EvoMap AI"}'
```

**开始使用吧!** 🚀

## 參考

- [[Serper Api Config]]


## 相關文檔

- [[api_batch_optimize]]
- [[asset07_api_batch_optimize]]
- [[03-openclaw_config_schema_verify]]
