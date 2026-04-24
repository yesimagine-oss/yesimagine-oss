---
title: "OpenClaw 瀏覽器自動化最佳實踐"
type: "concept"
category: "concept"
tags: ["best-practices", "optimization", "browser"]
created_at: "2026-04-14"
version: "1.0"
related: ["openclaw-browser-quickstart"]
---

# OpenClaw 瀏覽器自動化最佳實踐

## 性能優化

### 1. 使用命令鏈接

```bash
# ❌ 低效：多次啟動
agent-browser open https://example.com
agent-browser wait --load networkidle
