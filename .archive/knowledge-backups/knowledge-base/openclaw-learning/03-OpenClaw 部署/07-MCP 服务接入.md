# OpenClaw MCP 服务接入指南

**学习时间**: 2026-03-12 11:36
**难度**: ⭐⭐⭐ 进阶
**预计时间**: 40 分钟

---

## 📚 MCP 概述

### 什么是 MCP

**MCP (Model Context Protocol)** 是 OpenClaw 的插件协议，用于扩展 Agent 的工具调用能力。

### 支持的 MCP 服务

| 服务 | 功能 | 使用场景 |
|------|------|----------|
| 联网搜索 | 实时搜索互联网 | 新闻、资讯、最新信息 |
| 网页抓取 | 提取网页内容 | 文章、文档、数据 |
| 文件处理 | 读写本地文件 | 文档分析、数据处理 |
| 数据库 | 连接数据库 | 数据查询、分析 |

---

## 🔧 联网搜索 MCP 配置

### 步骤 1: 安装 MCP 服务

```bash
# 安装联网搜索 MCP
openclaw mcp install web-search

# 或手动安装
npm install -g @openclaw/mcp-web-search
```

### 步骤 2: 配置 MCP

编辑配置文件 `~/.openclaw/openclaw.json`:

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
          "language": "zh-CN"
        }
      }
    }
  }
}
```

### 步骤 3: 使用 MCP 服务

#### 方式 1: 直接在对话中使用

```
用户：搜索最新的 AI 新闻
Agent: [自动调用 web-search MCP]
```

#### 方式 2: 在 Cron 任务中使用

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

## 🌐 网页抓取 MCP 配置

### 步骤 1: 安装网页抓取 MCP

```bash
# 安装网页抓取 MCP
openclaw mcp install web-scraper

# 或手动安装
npm install -g @openclaw/mcp-web-scraper
```

### 步骤 2: 配置 MCP

```json
{
  "mcp": {
    "services": {
      "web-scraper": {
        "enabled": true,
        "config": {
          "timeout": 30000,
          "userAgent": "Mozilla/5.0 (compatible; OpenClaw/1.0)",
          "respectRobotsTxt": true
        }
      }
    }
  }
}
```

### 步骤 3: 使用示例

#### 抓取新闻网站

```bash
openclaw cron add \
  --name "tech-news" \
  --cron "0 18 * * *" \
  --message "请访问 https://36kr.com 获取今天的科技新闻，总结前 5 条" \
  --channel telegram \
  --announce
```

#### 抓取论文网站

```bash
openclaw cron add \
  --name "paper-digest" \
  --cron "0 9 * * 1" \
  --message '请使用 curl 命令执行以下请求获取论文数据：
curl -s "http://export.arxiv.org/api/query?search_query=all:%22llm+as+a+judge%22&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
解析返回的 XML 数据，列出前 5 篇论文，每篇包含：
1. 标题
2. 发布日期
3. 摘要总结（用中文，2-3 句话概括核心贡献）
4. arXiv 链接
5. 如果 XML 中包含 GitHub 代码链接也列出
按发布时间从新到旧排列。' \
  --channel dingtalk \
  --announce \
  --timeout-seconds 120
```

---

## 🔍 使用案例

### 案例 1: AI 新闻每日推送

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

**预期效果**:
```
📰 AI 日报 - 2026-03-12

1. OpenAI 发布 GPT-5，推理能力提升 40%
2. 谷歌推出新的多模态模型...
3. ...
```

---

### 案例 2: HuggingFace 热门模型

```bash
openclaw cron add \
  --name "hf-trending-models" \
  --cron "0 9 * * 1" \
  --tz "Asia/Shanghai" \
  --message '请使用 curl 命令执行以下请求获取 HuggingFace 上最近热门的大语言模型：
curl -s "https://hf-mirror.com/api/models?sort=trendingScore&direction=-1&limit=10&pipeline_tag=text-generation"
解析返回的 JSON 数据，列出前 10 个模型，每个包含：
1. 模型名称
2. 发布日期
3. 下载量和点赞数
4. 模型页面链接
重点标注最近一个月内新发布的模型，并用中文简要说明每个模型的特点。' \
  --channel dingtalk \
  --announce \
  --timeout-seconds 120
```

---

### 案例 3: GitHub 热门项目

```bash
openclaw cron add \
  --name "github-trending" \
  --cron "0 9 * * 1" \
  --tz "Asia/Shanghai" \
  --message '请获取过去一周内 GitHub 上新创建的热门项目（按 Star 数排序前 10），每个项目列出名称、Star 数、简介（中文翻译）、编程语言和链接，重点标注 Star 数超过 1000 的项目。请先用 date 命令计算 7 天前的日期，然后通过 GitHub Search API 的 created 参数筛选。' \
  --channel dingtalk \
  --announce \
  --timeout-seconds 120
```

---

## ⚙️ MCP 配置详解

### 完整配置示例

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
      },
      "web-scraper": {
        "enabled": true,
        "config": {
          "timeout": 30000,
          "userAgent": "Mozilla/5.0 (compatible; OpenClaw/1.0)",
          "respectRobotsTxt": true,
          "retryCount": 3
        }
      },
      "file-system": {
        "enabled": false,
        "config": {
          "allowedDirectories": ["~/documents", "~/downloads"],
          "maxFileSize": 10485760
        }
      }
    },
    "defaults": {
      "timeout": 30000,
      "maxRetries": 3
    }
  }
}
```

---

## 🔧 MCP 管理命令

```bash
# 查看已安装的 MCP 服务
openclaw mcp list

# 安装 MCP 服务
openclaw mcp install <service-name>

# 卸载 MCP 服务
openclaw mcp uninstall <service-name>

# 启用 MCP 服务
openclaw mcp enable <service-name>

# 禁用 MCP 服务
openclaw mcp disable <service-name>

# 测试 MCP 服务
openclaw mcp test <service-name>
```

---

## ⚠️ 常见问题

### Q1: MCP 服务无法加载

**检查**:
```bash
# 查看 MCP 状态
openclaw mcp list

# 查看日志
openclaw logs --grep mcp
```

**解决**:
```bash
# 重新安装
openclaw mcp uninstall <service>
openclaw mcp install <service>
```

---

### Q2: 网页抓取超时

**解决**:
```json
{
  "mcp": {
    "services": {
      "web-scraper": {
        "config": {
          "timeout": 60000,
          "retryCount": 3
        }
      }
    }
  }
}
```

---

### Q3: 搜索结果不准确

**解决**:
- 更换 SearXNG 实例
- 调整搜索参数
- 优化 Prompt

---

## ✅ 验收清单

- [ ] MCP 服务已安装
- [ ] 配置已更新
- [ ] 联网搜索测试通过
- [ ] 网页抓取测试通过
- [ ] Cron 任务已配置

---

**学习状态**: ✅ 已完成
**下一步**: 继续补充其他遗漏内容
