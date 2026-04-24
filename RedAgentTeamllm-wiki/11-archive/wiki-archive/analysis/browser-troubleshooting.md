---
category: analysis
created_at: '2026-04-14'
related:
- browser-best-practices
tags:
- troubleshooting
- debugging
- browser
title: OpenClaw 瀏覽器自動化故障排查
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
# OpenClaw 瀏覽器自動化故障排查

## 常見問題

### 1. Chrome 無法啟動

**症狀：**
```
Error: Chrome failed to launch
```

**解決方案：**
```bash
# 檢查 Chrome 安裝
which google-chrome

# 重新安裝 Chrome
agent-browser install

# 使用無沙盒模式
agent-browser open https://example.com --no-sandbox
```

### 2. 端口被占用

**症狀：**
```
Error: Port 18800 is already in use
```

**解決方案：**
```bash
# 查找占用進程
lsof -i :18800

# 殺死進程
kill -9 <PID>

# 或使用不同端口
agent-browser open https://example.com --cdp-port 18801
```

### 3. 元素找不到

**症狀：**
```
Error: Element @e1 not found
```

**解決方案：**
```bash
# 重新快照（DOM 可能已變化）
agent-browser snapshot -i

# 檢查元素是否還在
# 使用更穩定的引用（基於角色 + 名稱）
agent-browser click "@[button] 'Submit'"
```

### 4. 超時錯誤

**症狀：**
```
Error: Timeout after 30000ms
```

**解決方案：**
```bash
# 增加超時時間
agent-browser wait --load networkidle --timeout 60000

# 檢查網絡條件
# 使用更寬鬆的等待條件
agent-browser wait --load domcontentloaded
```

### 5. 記憶體不足

**症狀：**
```
Error: No available memory
```

**解決方案：**
```bash
# 關閉不需要的標籤頁
agent-browser close

# 使用更小的視口
agent-browser open https://example.com --width 1280 --height 720

# 增加 swap 空間
```

## 調試技巧

### 1. 啟用詳細日誌

```bash
agent-browser open https://example.com --verbose
```

### 2. 保存狀態

```bash
# 保存會話狀態
agent-browser state save session.json

# 從狀態恢復
agent-browser state load session.json
```

### 3. 視頻錄製

```bash
# 錄製操作過程
agent-browser video start
agent-browser open https://example.com
agent-browser video stop recording.mp4
```

## 參考

- [[browser-best-practices]]
- [[browser-commands-reference]]

---

**Red Agent Team | 2026-04-14**


## 相關文檔

- [[openclaw-browser-quickstart]]
- [[browser-use-cases]]
- [[openclaw-browser-complete-guide-index]]
