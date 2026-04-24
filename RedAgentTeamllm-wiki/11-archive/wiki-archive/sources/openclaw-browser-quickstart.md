---
category: source
created_at: '2026-04-14'
related:
- openclaw-browser-installation-guide
tags:
- quickstart
- browser
- tutorial
title: OpenClaw 無頭瀏覽器快速開始
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
# OpenClaw 無頭瀏覽器快速開始

## 5 分鐘第一個瀏覽器自動化

### 場景：自動打開網頁並截圖

```bash
# 1. 打開網頁
agent-browser open https://example.com

# 2. 等待加載
agent-browser wait --load networkidle

# 3. 截圖
agent-browser screenshot page.png

# 4. 查看結果
ls -la page.png
```

### 場景：自動填寫表單

```bash
# 1. 打開表單頁面
agent-browser open https://example.com/form

# 2. 獲取元素引用
agent-browser snapshot -i
# 輸出：@e1 [input email], @e2 [input password], @e3 [button] "Submit"

# 3. 填寫表單
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"

# 4. 提交
agent-browser click @e3

# 5. 等待並驗證
agent-browser wait --load networkidle
agent-browser screenshot result.png
```

### 場景：使用 Python 工具

```python
from browser_tool import BrowserTool

browser = BrowserTool(session_name="demo")
browser.open("https://example.com")
browser.snapshot()
browser.screenshot("page.png")
```

## 參考

- [[openclaw-browser-installation-guide]]
- [[openclaw-headless-browser-architecture]]

---

**Red Agent Team | 2026-04-14**


## 相關文檔

- [[browser-use-cases]]
- [[openclaw-docs-deliberation-20260413]]
- [[openclaw-learning-report]]
