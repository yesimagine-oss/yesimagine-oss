---
title: "OpenClaw 無頭瀏覽器架構設計"
type: "entity"
category: "entity"
tags: ["browser", "automation", "openclaw", "headless"]
created_at: "2026-04-14"
version: "1.0"
related: ["agent-browser-skill", "browser-tool-integration"]
---

# OpenClaw 無頭瀏覽器架構設計

## 核心問題

當前 AI Agent 瀏覽器自動化存在三大痛點：

1. **過度依賴人類交互** - 傳統工具（Selenium、Playwright）包含大量 UI/插件生態，不適合純 AI 自動化
2. **脆弱的元素定位** - CSS 選擇器、XPath 在 DOM 變化時容易失效
3. **缺乏自然語言接口** - 需要中間翻譯層將 AI 意圖轉換為代碼

