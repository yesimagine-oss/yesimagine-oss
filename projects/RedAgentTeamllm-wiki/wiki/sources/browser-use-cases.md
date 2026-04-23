---
category: source
created_at: '2026-04-14'
related:
- openclaw-browser-quickstart
tags:
- examples
- use-cases
- tutorial
title: OpenClaw 瀏覽器自動化使用示例
type: source
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
# OpenClaw 瀏覽器自動化使用示例

## 場景 1：自動登錄

```bash
# 打開登錄頁面
agent-browser open https://example.com/login

# 獲取元素
agent-browser snapshot -i
# @e1 [input email], @e2 [input password], @e3 [button] "Login"

# 填寫並提交
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3

# 等待並驗證
agent-browser wait --load networkidle
agent-browser screenshot dashboard.png
```

## 場景 2：數據抓取

```bash
# 打開列表頁
agent-browser open https://example.com/products

# 提取產品信息
agent-browser extract ".product-name"
agent-browser extract ".product-price"

# 翻頁
agent-browser click "@next-page"
agent-browser wait --load networkidle
```

## 場景 3：表單提交

```bash
# 打開表單
agent-browser open https://example.com/contact

# 填寫所有字段
agent-browser fill "@name" "John Doe"
agent-browser fill "@email" "john@example.com"
agent-browser fill "@message" "Hello!"

# 提交
agent-browser click "@submit"
```

## 場景 4：測試自動化

```bash
# 打開應用
agent-browser open https://myapp.com

# 執行測試步驟
agent-browser click "@login-btn"
agent-browser fill "@username" "test"
agent-browser fill "@password" "test123"
agent-browser click "@submit"

# 驗證結果
agent-browser screenshot test-result.png
```

## 參考

- [[browser-commands-reference]]
- [[openclaw-browser-quickstart]]

---

**Red Agent Team | 2026-04-14**


## 相關文檔

- [[openclaw-browser-complete-guide-index]]
- [[agent-browser-深度學習報告]]
- [[openclaw-headless-browser-architecture]]
