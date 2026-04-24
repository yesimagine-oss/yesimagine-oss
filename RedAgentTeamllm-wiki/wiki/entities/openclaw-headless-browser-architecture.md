---
category: entity
created_at: '2026-04-14'
related:
- agent-browser-skill
- browser-tool-integration
tags:
- browser
- automation
- openclaw
- headless
title: OpenClaw 無頭瀏覽器架構設計
type: entity
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
# OpenClaw 無頭瀏覽器架構設計

## 核心問題

當前 AI Agent 瀏覽器自動化存在三大痛點：

1. **過度依賴人類交互** - 傳統工具（Selenium、Playwright）包含大量 UI/插件生態，不適合純 AI 自動化
2. **脆弱的元素定位** - CSS 選擇器、XPath 在 DOM 變化時容易失效
3. **缺乏自然語言接口** - 需要中間翻譯層將 AI 意圖轉換為代碼

## 設計三原則

1. **完全無頭模式** - 砍掉所有人類交互層，只保留 DOM 渲染 + 無障礙樹快照
2. **ref-based 元素定位** - 使用 ARIA ID/角色 + 名稱定位（@e1, @e2）
3. **自然語言指令** - 內置指令解析層，直接接收 AI 的自然語言操作指令

## 核心架構

```
AI Agent (OpenClaw)
    ↓ 自然語言指令
browser_tool.py (Python 集成層)
    ↓ CLI 命令
agent-browser (Rust CLI)
    ↓ CDP 協議
Chrome/Lightpanda (無頭瀏覽器)
```

## 組件說明

| 組件 | 職責 | 位置 |
|------|------|------|
| OpenClaw | AI Agent，發出自然語言指令 | OpenClaw 核心 |
| browser_tool.py | Python 集成層，轉換指令為 CLI 命令 | tools/browser_tool.py |
| agent-browser | Rust CLI，執行瀏覽器操作 | /usr/bin/agent-browser |
| Chrome | 無頭瀏覽器，渲染頁面 | /usr/bin/google-chrome |

## 參考

- [[agent-browser-skill]]
- [[browser-tool-integration]]
- [[skill-development-guide]]

---

**Red Agent Team | 2026-04-14**
