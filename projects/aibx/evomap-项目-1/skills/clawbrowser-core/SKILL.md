---
name: ClawBrowser Core
description: OpenClaw 自研无头浏览器核心 - 基于 Chromium 的浏览器自动化引擎，支持 CDP 协议、ARIA 快照、自然语言交互
category: automation
tags: ["browser", "automation", "cdp", "aria", "headless", "clawbrowser", "web-scraping", "testing"]
version: 1.0.0
---

# ClawBrowser Core

## Trigger Signals
- `browser` -- 当需要浏览器自动化时触发
- `web_automation` -- 当需要网页交互时触发
- `headless_browser` -- 当需要无头浏览器时触发
- `cdp` -- 当需要 Chrome DevTools Protocol 时触发
- `aria_snapshot` -- 当需要无障碍树快照时触发
- `web_scraping` -- 当需要网页抓取时触发

## Overview

ClawBrowser Core 是 OpenClaw 自主研发的浏览器自动化核心，基于 Chromium 和 CDP 协议，专为 AI Agent 设计：

### 核心特性
- **无头模式运行** - 节省资源，适合服务器环境
- **ARIA 无障碍树快照** - AI 友好的页面理解方式
- **自然语言交互** - ref-based 元素定位（@e1, @e2...）
- **会话隔离** - 多任务并行处理
- **CDP 协议支持** - 完整的 Chrome DevTools Protocol

### 应用场景
- 网页自动化测试
- 数据采集与抓取
- 表单自动填充
- 截图与 PDF 导出
- 单页应用（SPA）测试

## Strategy

### 1. 启动浏览器

```bash
# ClawBrowser Core 自动启动 Chromium 无头模式
agent-browser open https://example.com
```

### 2. 导航到页面

```python
browser(action="navigate", url="https://example.com")
browser(action="wait", loadState="networkidle")
```

### 3. 获取页面快照

```python
snapshot = browser(action="snapshot")
# 返回 ARIA 树：heading, link, button 等元素及 ref 引用
```

### 4. 元素交互

```python
# 点击
browser(action="click", ref="@e1")

# 填充
browser(action="fill", ref="@e2", text="test input")

# 获取文本
text = browser(action="text", ref="@e3")
```

### 5. 高级功能

```python
# 截图
browser(action="screenshot", path="page.png")

# PDF
browser(action="pdf", path="page.pdf")

# JS 执行
result = browser(action="eval", script="document.title")
```

## Constraints

- 最大并发会话数：5
- 单会话超时：60 秒
- 支持协议：CDP v1.3+
- 浏览器版本：Chromium 146+
- 内存占用：~50MB/会话

## Validation

```bash
# 检查浏览器状态
curl http://127.0.0.1:port/json/version

# 测试导航
agent-browser navigate https://example.com
agent-browser snapshot

# 性能测试
time agent-browser open https://example.com
# 预期：<2 秒
```

## Performance

| 操作 | 目标时间 |
|------|---------|
| 冷启动 | <2 秒 |
| 快照获取 | <500ms |
| 元素定位 | <100ms |
| 内存占用 | ~50MB/会话 |

## Troubleshooting

**Q: 浏览器启动失败**
```
A: 检查 Chromium 是否安装
```

**Q: CDP 连接超时**
```
A: 检查端口是否被占用
```

**Q: 快照获取为空**
```
A: 等待页面加载完成
```

## License

MIT License

## Changelog

### v1.0.0 (2026-04-04)
- 初始发布
- 支持 CDP 协议
- ARIA 快照功能
- 自然语言交互

## 參考

- [[Final-Skills-Status-Report]]
- [[首发帖子-Github-Skill-安装教程]]
- [[Skills-Installation-Status]]
