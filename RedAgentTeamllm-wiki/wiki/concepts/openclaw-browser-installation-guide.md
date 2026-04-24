---
category: concept
created_at: '2026-04-14'
related:
- openclaw-headless-browser-architecture
tags:
- installation
- browser
- openclaw
- setup
title: OpenClaw 無頭瀏覽器安裝配置指南
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
# OpenClaw 無頭瀏覽器安裝配置指南

## 從 0 開始安裝

### 步驟 1：安裝 agent-browser

```bash
# 全局安裝（推薦）
npm install -g agent-browser

# 或使用 Homebrew (macOS)
brew install agent-browser

# 或使用 Cargo (Rust)
cargo install agent-browser
```

### 步驟 2：下載 Chrome

```bash
# 首次使用需要下載 Chrome
agent-browser install
```

### 步驟 3：部署 browser_tool.py

```bash
# 複製到 tools 目錄
cp /path/to/browser_tool.py /home/admin/.openclaw/workspace/tools/

# 測試
python3 /home/admin/.openclaw/workspace/tools/browser_tool.py --help
```

### 步驟 4：集成到 OpenClaw

```bash
# 配置 OpenClaw 使用 browser_tool
# 編輯 openclaw.json 添加 browser 工具
```

## 驗證安裝

```bash
# 測試打開網頁
agent-browser open https://example.com

# 測試快照
agent-browser snapshot -i

# 測試 Python 工具
python3 tools/browser_tool.py open https://example.com
```

## 常見問題

| 問題 | 解決方案 |
|------|---------|
| Chrome 下載失敗 | 檢查網絡，使用代理 |
| 端口被占用 | 更改 CDP 端口 |
| 權限不足 | 使用 sudo 或 --no-sandbox |

## 參考

- [[openclaw-headless-browser-architecture]]
- [[skill-development-guide]]

---

**Red Agent Team | 2026-04-14**


## 相關文檔

- [[INSTALL-VALIDATOR-GUIDE]]
- [[openclaw-browser-quickstart]]
- [[browser-use-cases]]
