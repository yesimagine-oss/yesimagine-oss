---
title: "OpenClaw 瀏覽器自動化使用示例"
type: "source"
category: "source"
tags: ["examples", "use-cases", "tutorial"]
created_at: "2026-04-14"
version: "1.0"
related: ["openclaw-browser-quickstart"]
---

# OpenClaw 瀏覽器自動化使用示例

## 場景 1：自動登錄

```bash
# 打開登錄頁面
agent-browser open https://example.com/login

# 獲取元素
agent-browser snapshot -i
