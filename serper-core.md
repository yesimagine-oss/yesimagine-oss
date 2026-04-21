# Serper.dev 核心知识库（精简版）

**版本:** 2.0 精简版 | **更新:** 2026-03-21 | **大小:** 7KB

---

## 🔑 账户配置

```
邮箱：red@unvw.com | 密码：red753951
API Key: 01529847d4aa3cf47b86ca87d28519110db06390
配置：/home/admin/.openclaw/workspace/.env.serper
免费额度：2,500 次/月
```

---

## 🎯 10 种 API 端点

| 端点 | 命令 | 用途 |
|------|------|------|
| `/search` | `search` | 网页搜索 |
| `/images` | `images` | 图片搜索 |
| `/news` | `news` | 新闻搜索 |
| `/maps` | `maps` | 地图搜索 |
| `/places` | `places` | 地点搜索 |
| `/videos` | `videos` | 视频搜索 |
| `/shopping` | `shopping` | 购物搜索 |
| `/scholar` | `scholar` | 学术搜索 |
| `/patents` | `patents` | 专利搜索 |
| `/autocomplete` | `autocomplete` | 搜索建议 |

---

## 🔧 核心参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `q` | 关键词（必填） | `"q": "AI"` |
| `gl` | 国家 | `"gl": "us"` |
| `hl` | 语言 | `"hl": "en"` |
| `location` | 地理位置 | `"location": "Beijing"` |
| `tbs` | 时间范围 | `"tbs": "qdr:w"` (周) |

**时间范围:** `qdr:h`(时) `qdr:d`(天) `qdr:w`(周) `qdr:m`(月) `qdr:y`(年)

---

## 🚀 快速使用

### curl
```bash
curl -X POST https://google.serper.dev/search \
  -H 'X-API-KEY: 01529847d4aa3cf47b86ca87d28519110db06390' \
  -H 'Content-Type: application/json' \
  -d '{"q": "AI agent"}'
```

### Python
```python
import requests

def search(q, endpoint="search", **params):
    r = requests.post(f"https://google.serper.dev/{endpoint}",
        headers={'X-API-KEY': '01529847d4aa3cf47b86ca87d28519110db06390', 'Content-Type': 'application/json'},
        json={"q": q, **params})
    return r.json()
```

### 命令行
```bash
uv run skills/serper/scripts/serper.py search "AI agent"
```

---

## 💡 核心场景

| 场景 | 命令 |
|------|------|
| 资料收集 | `search "topic" -n 20` |
| 热点监控 | `news "topic" --time-range week` |
| 找场地 | `places "art space" --location "Jinan"` |
| 找图片 | `images "topic"` |
| 解决问题 | `search "error solution"` |

---

## 💰 定价

| 方案 | 价格 | 额度 | 单价 |
|------|------|------|------|
| 免费 | $0 | 2.5k | $0 |
| Starter | $50 | 50k | $1/1k |
| Standard | $375 | 500k | $0.75/1k |

---

## ⚠️ 注意

- 免费额度 2,500 次/月
- QPS 限制：5 次/秒（免费）
- serper.dev 无需代理，API 调用可能需要

---

## 📁 完整文档

- 详细版：`serper-knowledge-base.md` (11KB)
- 进阶分析：`serper-advanced-analysis.md` (9KB)
- 提升计划：`serper-gap-analysis.md` (5KB)
- 索引：`SERPER-INDEX.md` (6KB)
