---
category: automation
created_at: '2026-04-14'
description: OpenClaw 無頭瀏覽器自動化 - 基於 agent-browser 的瀏覽器自動化 Skill，支持 CDP 協議、ARIA 快照、自然語言交互
name: clawbrowser
tags:
- browser
- automation
- cdp
- aria
- headless
- agent-browser
- web-scraping
- testing
version: 2.0.0

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
# ClawBrowser

## Trigger Signals
- `browser` - 瀏覽器自動化
- `web_automation` - 網頁交互
- `headless_browser` - 無頭瀏覽器
- `cdp` - Chrome DevTools Protocol
- `aria_snapshot` - ARIA 快照
- `web_scraping` - 網頁抓取
- `screenshot` - 截圖

## Overview

ClawBrowser 是基於 agent-browser 的 OpenClaw 瀏覽器自動化 Skill，專為 AI Agent 設計：

### 核心特性
- **無頭模式** - 節省資源，適合服務器環境
- **ARIA 快照** - AI 友好的頁面理解
- **ref-based 定位** - @e1, @e2 元素引用
- **自然語言指令** - 直接接收 AI 指令
- **會話管理** - 多任務並行

### 架構
```
OpenClaw Agent
    ↓ 自然語言指令
clawbrowser Skill
    ↓ agent-browser CLI
Chrome (無頭)
```

## Installation

### 前置要求
```bash
# 1. 安裝 agent-browser
npm install -g agent-browser
agent-browser install

# 2. 驗證安裝
agent-browser --help
```

### 依賴
- Node.js v18+
- Chrome/Chromium
- agent-browser CLI

## Commands

### 基本命令

| 命令 | 說明 | 示例 |
|------|------|------|
| `open` | 打開網頁 | `open https://example.com` |
| `snapshot` | 獲取快照 | `snapshot -i` |
| `click` | 點擊元素 | `click @e1` |
| `fill` | 填寫輸入 | `fill @e1 "text"` |
| `screenshot` | 截圖 | `screenshot page.png` |
| `close` | 關閉頁面 | `close` |

### 高級命令

| 命令 | 說明 | 示例 |
|------|------|------|
| `wait` | 等待條件 | `wait --load networkidle` |
| `extract` | 提取內容 | `extract "h1"` |
| `evaluate` | 執行 JS | `evaluate "document.title"` |
| `pdf` | 生成 PDF | `pdf output.pdf` |

## Usage

### 場景 1：打開網頁並截圖
```bash
clawbrowser open https://example.com
clawbrowser wait --load networkidle
clawbrowser screenshot page.png
```

### 場景 2：自動填寫表單
```bash
clawbrowser open https://example.com/form
clawbrowser snapshot -i
# @e1 [input email], @e2 [input password], @e3 [button] "Submit"
clawbrowser fill @e1 "user@example.com"
clawbrowser fill @e2 "password123"
clawbrowser click @e3
```

### 場景 3：數據抓取
```bash
clawbrowser open https://example.com/products
clawbrowser snapshot -i
clawbrowser extract ".product-name"
clawbrowser extract ".product-price"
```

## Configuration

### 會話管理
```bash
# 使用命名會話
clawbrowser open https://example.com --session mytask
clawbrowser click @e1 --session mytask
clawbrowser close --session mytask
```

### 超時設置
```bash
# 設置超時時間
clawbrowser wait --load networkidle --timeout 10000
```

## Best Practices

### 1. 命令鏈接
```bash
# 高效：一次啟動
clawbrowser open https://example.com && \
  clawbrowser wait --load networkidle && \
  clawbrowser snapshot -i
```

### 2. 按需快照
```bash
# 只在需要時快照
clawbrowser snapshot -i
clawbrowser click @e1 && \
  clawbrowser fill @e2 "text" && \
  clawbrowser snapshot -i
```

### 3. 錯誤處理
```bash
# 設置超時
clawbrowser wait --load networkidle --timeout 10000

# 重試機制
for i in {1..3}; do
  clawbrowser open https://example.com && break || sleep 2
done
```

## Troubleshooting

### Chrome 無法啟動
```bash
# 重新安裝 Chrome
agent-browser install

# 使用無沙盒模式
clawbrowser open https://example.com --no-sandbox
```

### 端口被占用
```bash
# 使用不同端口
clawbrowser open https://example.com --cdp-port 18801
```

### 元素找不到
```bash
# 重新快照（DOM 可能已變化）
clawbrowser snapshot -i
```

## References

- [[openclaw-headless-browser-architecture]] - 架構設計
- [[openclaw-browser-installation-guide]] - 安裝配置
- [[openclaw-browser-quickstart]] - 快速開始
- [[browser-cdp-protocol]] - CDP 協議
- [[browser-commands-reference]] - 命令參考
- [[browser-use-cases]] - 使用示例
- [[browser-best-practices]] - 最佳實踐
- [[browser-troubleshooting]] - 故障排查

## Version History

| 版本 | 日期 | 變更 |
|------|------|------|
| 2.0.0 | 2026-04-14 | 基於 agent-browser 重構 |
| 1.0.0 | 2026-04-04 | 初代 clawbrowser-core |

---

**Red Agent Team | 2026-04-14**
