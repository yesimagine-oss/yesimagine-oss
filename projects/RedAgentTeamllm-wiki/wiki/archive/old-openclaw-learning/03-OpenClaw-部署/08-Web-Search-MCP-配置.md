---
category: llm
created_at: '2026-04-14'
tags:
- llm
- openclaw
- web
- search
- mcp
- 配置
title: 08 Web Search Mcp 配置
type: general
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
# OpenClaw Web Search MCP 配置

**学习时间**: 2026-03-12 11:46
**难度**: ⭐⭐ 中等
**预计时间**: 30 分钟

---

## 📚 概述

### 什么是 Web Search MCP

Web Search MCP 是 OpenClaw 的联网搜索插件，让 AI 能够访问实时互联网信息。

### 官方文档链接

https://help.aliyun.com/zh/model-studio/web-search-for-coding-plan

---

## 🔧 安装步骤

### 步骤 1: 添加联网搜索 MCP

```bash
# 通过 OpenClaw 添加
openclaw mcp add web-search

# 或手动配置
```

### 步骤 2: 配置 MCP

编辑 `~/.openclaw/openclaw.json`:

```json
{
  "mcp": {
    "enabled": true,
    "services": {
      "web-search": {
        "enabled": true,
        "provider": "searxng",
        "config": {
          "instanceUrl": "https://searx.be",
          "maxResults": 10,
          "language": "zh-CN",
          "categories": ["general", "news", "science"]
        }
      }
    }
  }
}
```

---

## 🌐 配置选项

### SearXNG 公共实例

| 实例 | 地址 | 推荐度 |
|------|------|--------|
| SearX.BE | https://searx.be | ⭐⭐⭐⭐⭐ |
| SearX.NG | https://searx.ng | ⭐⭐⭐⭐ |
| SearX.Me | https://searx.me | ⭐⭐⭐⭐ |
| 自建实例 | 自行部署 | ⭐⭐⭐⭐⭐ |

### 配置参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| instanceUrl | SearXNG 实例地址 | https://searx.be |
| maxResults | 最大返回结果数 | 10 |
| language | 搜索语言 | zh-CN |
| categories | 搜索分类 | ["general"] |
| timeout | 超时时间（毫秒） | 30000 |

---

## 💬 使用示例

### 基础搜索

```
用户：搜索最新的 AI 新闻
Agent: [自动调用 web-search MCP]
```

### 在 Cron 任务中使用

```bash
openclaw cron add \
  --name "ai-daily-news" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --message "请访问 https://www.aibase.com/zh/daily 获取今天的 AI 日报，总结前 10 条最重要的 AI 新闻，用简洁的中文列表形式输出，每条包含标题和一句话摘要" \
  --channel dingtalk \
  --announce \
  --timeout-seconds 120
```

---

## 🔍 自建 SearXNG 实例

### Docker 部署

```bash
# 1. 创建 docker-compose.yml
cat > docker-compose.yml << EOF
version: '3'
services:
  searxng:
    image: searxng/searxng:latest
    ports:
      - "8080:8080"
    volumes:
      - ./searxng:/etc/searxng
    environment:
      - SEARXNG_BASE_URL=http://localhost:8080
EOF

# 2. 启动服务
docker-compose up -d

# 3. 访问 http://localhost:8080
```

### 配置 OpenClaw 使用自建实例

```json
{
  "mcp": {
    "services": {
      "web-search": {
        "enabled": true,
        "provider": "searxng",
        "config": {
          "instanceUrl": "http://localhost:8080",
          "maxResults": 10,
          "language": "zh-CN"
        }
      }
    }
  }
}
```

---

## ⚠️ 常见问题

### Q1: 搜索失败

**检查**:
```bash
# 测试实例连通性
curl -I https://searx.be

# 查看 MCP 日志
openclaw logs --grep mcp
```

**解决**:
- 更换 SearXNG 实例
- 增加超时时间
- 检查网络连接

---

### Q2: 搜索结果不准确

**解决**:
```json
{
  "mcp": {
    "services": {
      "web-search": {
        "config": {
          "language": "zh-CN",
          "categories": ["news", "science"]
        }
      }
    }
  }
}
```

---

### Q3: MCP 服务无法加载

**检查**:
```bash
# 查看 MCP 状态
openclaw mcp list

# 重启服务
openclaw gateway restart
```

---

## ✅ 验收清单

- [ ] MCP 服务已安装
- [ ] SearXNG 实例已配置
- [ ] 搜索功能测试通过
- [ ] Cron 任务可使用

---

**学习状态**: ✅ 已完成
**下一步**: 继续补充其他遗漏内容

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[MCP 集成完全指南]]
- [[08-hunter_deferred_claim]]
- [[08-hunter_deferred_claim_final]]
