---
category: concept
created_at: '2026-04-14'
related:
- openclaw-headless-browser-architecture
tags:
- cdp
- aria
- protocol
- browser
title: CDP 協議與 ARIA Refs 核心概念
type: concept
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
# CDP 協議與 ARIA Refs 核心概念

## CDP (Chrome DevTools Protocol)

### 什麼是 CDP

CDP 是 Chrome 的遠程調試協議，允許外部工具控制瀏覽器。

### 核心功能

| 功能 | CDP Domain | 說明 |
|------|-----------|------|
| 導航 | Page | 打開網頁、等待加載 |
| 操作 | Input | 點擊、輸入、滾動 |
| 提取 | DOM | 獲取元素信息 |
| 截圖 | Page | 頁面截圖 |

### CDP 連接

```bash
# Chrome 啟動時開啟 CDP 端口
google-chrome --remote-debugging-port=18800

# agent-browser 連接
agent-browser --cdp-port 18800 snapshot
```

## ARIA Refs (無障礙引用)

### 什麼是 ARIA Refs

ARIA (Accessible Rich Internet Applications) 引用是基於無障礙樹的元素定位方式。

### 為什麼用 ARIA Refs

| 傳統方式 | ARIA Refs |
|---------|-----------|
| CSS 選擇器：`.btn.primary` | 引用：`@e1` |
| XPath：`//button[@class='submit']` | 引用：`@e3 [button] "Submit"` |
| DOM 變化時失效 | 基於角色 + 名稱，更穩定 |

### ARIA Refs 格式

```
@e1 [input type="email"]
@e2 [button] "Submit"
@e3 [link] "Learn More"
```

### 使用示例

```bash
# 獲取引用
agent-browser snapshot -i

# 使用引用
agent-browser click @e2
agent-browser fill @e1 "user@example.com"
```

## 參考

- [[openclaw-headless-browser-architecture]]
- [[openclaw-browser-quickstart]]

---

**Red Agent Team | 2026-04-14**


## 相關文檔

- [[browser-use-cases]]
- [[config-modification-safety-protocol-20260413]]
- [[deep-protocol-diagnostics-report-20260413]]
