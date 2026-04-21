# 🔧 百度搜索配置指南

**创建时间:** 2026-03-15 17:12 GMT+8
**状态:** 需要配置

---

## ❌ 当前问题

| 搜索引擎 | 状态 | 说明 |
|---------|------|------|
| **Google (Serper)** | ✅ 可用 | 但国内内容有限 |
| **SearXNG** | ✅ 可用 | 国内源有限 |
| **百度** | ❌ 未配置 | 需要 API 或配置 |

---

## 🔧 解决方案

### 方案 A: 配置 SearXNG 百度引擎

**步骤:**

1. **编辑 SearXNG 配置**
```bash
sudo nano /etc/searxng/settings.yml
```

2. **添加百度引擎**
```yaml
engines:
  - name: 百度
    engine: json_engine
    search_url: https://www.baidu.com/s?wd={query}&rn=10&pn={pageno}&ie=utf-8&oe=utf-8
    url: https://www.baidu.com/link?url={url}
    title: {title}
    content: {abstract}
    pagenum_query: pn
    max_page: 10
    categories: general
    language: zh-CN
    disabled: false
```

3. **重启 SearXNG**
```bash
sudo systemctl restart searxng
```

---

### 方案 B: 申请百度 API

**步骤:**

1. **访问百度开放平台**
```
https://openapi.baidu.com/
```

2. **创建应用获取 API Key**

3. **配置到 OpenClaw**
```bash
export BAIDU_API_KEY="your_key"
export BAIDU_SECRET_KEY="your_secret"
```

---

### 方案 C: 使用第三方百度搜索 API

**推荐服务:**

| 服务 | 价格 | 说明 |
|------|------|------|
| **RapidAPI 百度** | $5-50/月 | 封装的百度 API |
| **ScraperAPI** | $29+/月 | 支持百度爬虫 |
| **Zenserp** | $19+/月 | 多引擎搜索 |

---

### 方案 D: 手动提供搜索结果 (临时)

**最直接的方式:**

1. 您在百度搜索
2. 复制搜索结果给我
3. 我分析和记录

---

## 📝 临时解决方案

**当前可用搜索:**

```bash
# 1. SearXNG (已配置)
cd ~/.openclaw/workspace/skills/searxng
uv run scripts/searxng.py search "关键词" -n 15

# 2. Serper API (Google)
curl -X POST https://google.serper.dev/search \
  -H "X-API-KEY: 01529847d4aa3cf47b86ca87d28519110db06390" \
  -d '{"q": "关键词"}'
```

---

## 🙏 请求帮助

**老胡，请您:**

1. **百度搜索关键词:** `胡宏基 导演`
2. **复制前 10 条结果** (标题 + 链接)
3. **发送给我**

**我立刻记录并分析！**

---

**预计解决时间:** 
- 方案 A (SearXNG 配置): 30 分钟
- 方案 B (百度 API): 1-2 小时
- 方案 C (第三方): 10 分钟
- 方案 D (手动): 立即
