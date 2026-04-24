---
category: concept
created_at: '2026-04-14'
related:
- openclaw-browser-quickstart
tags:
- best-practices
- optimization
- browser
title: OpenClaw 瀏覽器自動化最佳實踐
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
# OpenClaw 瀏覽器自動化最佳實踐

## 性能優化

### 1. 使用命令鏈接

```bash
# ❌ 低效：多次啟動
agent-browser open https://example.com
agent-browser wait --load networkidle
agent-browser snapshot -i

# ✅ 高效：一次啟動
agent-browser open https://example.com && \
  agent-browser wait --load networkidle && \
  agent-browser snapshot -i
```

### 2. 合理使用快照

```bash
# ❌ 過度快照
agent-browser snapshot -i
agent-browser click @e1
agent-browser snapshot -i  # 不需要
agent-browser fill @e2 "text"
agent-browser snapshot -i  # 不需要

# ✅ 按需快照
agent-browser snapshot -i
agent-browser click @e1 && \
  agent-browser fill @e2 "text" && \
  agent-browser snapshot -i  # 只在需要時
```

### 3. 會話復用

```bash
# 使用命名會話
agent-browser open https://example.com --session mytask
agent-browser click @e1 --session mytask
agent-browser close --session mytask
```

## 錯誤處理

### 1. 設置超時

```bash
# 避免無限等待
agent-browser wait --load networkidle --timeout 10000
```

### 2. 驗證元素存在

```bash
# 先快照，再操作
agent-browser snapshot -i
# 確認 @e1 存在後再點擊
agent-browser click @e1
```

### 3. 重試機制

```bash
# 失敗重試
for i in {1..3}; do
  agent-browser open https://example.com && break || sleep 2
done
```

## 安全實踐

### 1. 不存儲敏感信息

```bash
# ❌ 不要在命令中直接寫密碼
agent-browser fill @password "mysecretpassword"

# ✅ 使用環境變量
agent-browser fill @password "$BROWSER_PASSWORD"
```

### 2. 使用無頭模式

```bash
# 服務器環境使用無頭模式
agent-browser open https://example.com --headless
```

## 參考

- [[browser-commands-reference]]
- [[browser-use-cases]]

---

**Red Agent Team | 2026-04-14**


## 相關文檔

- [[openclaw-browser-quickstart]]
- [[openclaw-browser-complete-guide-index]]
- [[agent-browser-深度學習報告]]
