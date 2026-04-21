# Serper API 快速使用指南

**创建时间:** 2026-03-21  
**用途:** 快速查阅，立即上手  

---

## 🚀 30 秒开始

### 1. 测试 API

```bash
curl --request POST \
  --url https://google.serper.dev/search \
  --header 'X-API-KEY: 01529847d4aa3cf47b86ca87d28519110db06390' \
  --header 'Content-Type: application/json' \
  --data '{"q": "test"}'
```

### 2. 使用技能

```bash
# Web 搜索
uv run /home/admin/.openclaw/workspace/skills/serper/scripts/serper.py search "AI agent"

# 图片搜索
uv run /home/admin/.openclaw/workspace/skills/serper/scripts/serper.py images "robot"

# 新闻搜索
uv run /home/admin/.openclaw/workspace/skills/serper/scripts/serper.py news "AI technology"
```

### 3. 让我搜索

直接对我说：
- "搜索 AI agent 最新应用"
- "找一下济南的艺术空间"
- "看看最近有什么纪录片获奖"

---

## 📋 10 种搜索类型

| 类型 | 命令 | 示例 |
|------|------|------|
| **Web** | `search` | `search "AI agent"` |
| **图片** | `images` | `images "robot"` |
| **新闻** | `news` | `news "AI technology"` |
| **地图** | `maps` | `maps "coffee shop" --location "Beijing"` |
| **地点** | `places` | `places "art gallery" --location "Jinan"` |
| **视频** | `videos` | `videos "documentary"` |
| **购物** | `shopping` | `shopping "camera"` |
| **学术** | `scholar` | `scholar "machine learning"` |
| **专利** | `patents` | `patents "AI"` |
| **建议** | `autocomplete` | `autocomplete "artificial int"` |

---

## 🔧 常用参数

### 国家代码 (`--country`)

```bash
search "AI" --country us    # 美国
search "AI" --country cn    # 中国
search "AI" --country jp    # 日本
```

### 语言代码 (`--language`)

```bash
search "AI" --language en   # 英语
search "AI" --language zh-CN # 中文
search "AI" --language ja   # 日语
```

### 时间范围 (`--time-range`)

```bash
news "AI" --time-range hour  # 最近 1 小时
news "AI" --time-range day   # 最近 1 天
news "AI" --time-range week  # 最近 1 周
news "AI" --time-range month # 最近 1 月
news "AI" --time-range year  # 最近 1 年
```

### 结果数量 (`-n`)

```bash
search "AI" -n 10   # 10 个结果（默认）
search "AI" -n 50   # 50 个结果
search "AI" -n 100  # 100 个结果
```

### 输出格式 (`--format`)

```bash
search "AI" --format json    # JSON 格式
search "AI" --format text    # 文本格式（默认）
```

---

## 💡 实际场景

### 场景 1: 找灵感

```bash
# 搜索纪录片题材
uv run .../serper.py search "western china documentary award"

# 搜索相关图片
uv run .../serper.py images "western china landscape"
```

### 场景 2: 找场地

```bash
# 搜索济南艺术空间
uv run .../serper.py places "art space" --location "Jinan, China"

# 搜索北京展览场地
uv run .../serper.py places "exhibition venue" --location "Beijing, China"
```

### 场景 3: 监控动态

```bash
# 最近 1 周的行业新闻
uv run .../serper.py news "AI agent" --time-range week

# 最近 1 月的艺术展览
uv run .../serper.py news "art exhibition" --time-range month
```

### 场景 4: 解决问题

```bash
# 搜索技术问题
uv run .../serper.py search "Feishu API permission error solution"

# 搜索最佳实践
uv run .../serper.py search "OpenClaw skill development best practices"
```

---

## ⚠️ 注意事项

### 额度

- **免费额度:** 2,500 次/月
- **当前使用:** 查看 Dashboard
- **超额处理:** 购买额度或等下月

### 限制

- **免费 QPS:** 5 次/秒
- **结果数量:** 最多 100 个/次
- **缓存时间:** 搜索结果有缓存

### 代理

- **serper.dev:** ✅ 无需代理
- **API 调用:** ⚠️ 服务器可能需要代理

---

## 📚 完整文档

- **知识库:** `/home/admin/.openclaw/workspace/serper-knowledge-base.md`
- **配置文件:** `/home/admin/.openclaw/workspace/.env.serper`
- **技能位置:** `/home/admin/.openclaw/workspace/skills/serper/`

---

## 🎯 立即开始

**对我下命令:**
- "搜索 [任何话题]"
- "找 [某物] 的图片"
- "看看 [某话题] 的最新新闻"

**我会立即使用 Serper API 为您搜索！** 🔍
