---
name: clawbrowser-core
description: OpenClaw 無頭瀏覽器自動化 - 基於 agent-browser 的瀏覽器自動化 Skill，支持 CDP 協議、ARIA 快照、自然語言交互
category: automation
tags: ["browser", "automation", "cdp", "aria", "headless", "agent-browser", "web-scraping", "testing"]
version: 2.0.0
created_at: "2026-04-14"
author: "Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨..."
---

# ClawBrowser v2.0.0

---

## Trigger Signals
- `browser` - 瀏覽器自動化
- `web_automation` - 網頁交互
- `headless_browser` - 無頭瀏覽器
- `cdp` - Chrome DevTools Protocol
- `aria_snapshot` - ARIA 快照
- `web_scraping` - 網頁抓取
- `screenshot` - 截圖

---

## 功能介紹

### v1.0.0 核心功能（基礎）

- **無頭模式運行** - 節省資源，適合服務器環境
- **ARIA 無障礙樹快照** - AI 友好的頁面理解方式
- **自然語言交互** - ref-based 元素定位（@e1, @e2...）
- **會話隔離** - 多任務並行處理
- **CDP 協議支持** - 完整的 Chrome DevTools Protocol

### v2.0.0 升級功能（新增）

- **基於 agent-browser** - 使用成熟的 Rust CLI，更穩定可靠
- **簡化安裝** - npm 一鍵安裝，無需複雜配置
- **完整 Python 集成** - browser_tool.py 提供完整 API
- **3 個實用示例** - 截圖、表單、抓取，開箱即用
- **完整知識庫** - 8 篇文檔支持，從 0 到精通
- **自然語言指令** - 直接說「打開 github.com」即可執行

---

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

**⚠️ 抓取範圍說明（待測試）：**
- ✅ 公開網頁數據（產品、新聞、標題）
- ⚠️ 微信公眾號（需登錄，待測試）
- ⚠️ 需要登錄的網站（需保存會話，待測試）
- ❌ 有強反爬蟲的網站（可能無法抓取）

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
