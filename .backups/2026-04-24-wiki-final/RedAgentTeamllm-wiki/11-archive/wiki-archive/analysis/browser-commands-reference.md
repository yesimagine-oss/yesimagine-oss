---
category: analysis
created_at: '2026-04-14'
related:
- openclaw-browser-quickstart
tags:
- api
- commands
- reference
title: Agent-Browser 完整命令參考
type: analysis
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
# Agent-Browser 完整命令參考

## 核心命令

### 導航命令

| 命令 | 說明 | 示例 |
|------|------|------|
| `open` | 打開網頁 | `agent-browser open https://example.com` |
| `wait` | 等待條件 | `agent-browser wait --load networkidle` |
| `close` | 關閉頁面 | `agent-browser close` |

### 快照命令

| 命令 | 說明 | 示例 |
|------|------|------|
| `snapshot` | 獲取無障礙樹 | `agent-browser snapshot -i` |
| `screenshot` | 截圖 | `agent-browser screenshot page.png` |
| `pdf` | 生成 PDF | `agent-browser pdf output.pdf` |

### 交互命令

| 命令 | 說明 | 示例 |
|------|------|------|
| `click` | 點擊元素 | `agent-browser click @e1` |
| `fill` | 填寫輸入框 | `agent-browser fill @e1 "text"` |
| `select` | 選擇選項 | `agent-browser select @e1 "option"` |
| `hover` | 懸停元素 | `agent-browser hover @e1` |

### 提取命令

| 命令 | 說明 | 示例 |
|------|------|------|
| `extract` | 提取內容 | `agent-browser extract "h1"` |
| `evaluate` | 執行 JS | `agent-browser evaluate "document.title"` |

## 常用參數

### snapshot 參數

| 參數 | 說明 | 示例 |
|------|------|------|
| `-i` | 交互式輸出 | `snapshot -i` |
| `--refs aria` | 使用 ARIA refs | `snapshot --refs aria` |
| `--depth 3` | 深度限制 | `snapshot --depth 3` |

### wait 參數

| 參數 | 說明 | 示例 |
|------|------|------|
| `--load networkidle` | 等待網絡空閒 | `wait --load networkidle` |
| `--selector` | 等待元素 | `wait --selector "#loaded"` |
| `--timeout 5000` | 超時時間 | `wait --timeout 5000` |

## 命令鏈接

```bash
# 鏈接多個命令
agent-browser open https://example.com && \
  agent-browser wait --load networkidle && \
  agent-browser snapshot -i
```

## 參考

- [[openclaw-browser-quickstart]]
- [[browser-cdp-protocol]]

---

**Red Agent Team | 2026-04-14**


## 相關文檔

- [[browser-use-cases]]
- [[20-validation_commands_image_analysis]]
- [[feishu-quick-reference]]
