---
category: llm
created_at: '2026-04-14'
tags:
- llm
- 會話管理學習報告
- openclaw
title: Session Management Study
type: general
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
# 會話管理學習報告

**學習時間**: 2026-03-24 17:32  
**學習主題**: OpenClaw 歷史對話管理與清理機制  
**學習目標**: 理解會話存儲機制，制定自動化清理策略

---

## 📚 核心發現

### 1️⃣ OpenClaw 內建清理命令

```bash
# 預覽清理效果（不實際刪除）
openclaw sessions cleanup --dry-run

# 執行清理
openclaw sessions cleanup --enforce

# 針對所有 agent 清理
openclaw sessions cleanup --all-agents --dry-run

# 保護特定會話不被清理
openclaw sessions cleanup --active-key "agent:main:main" --enforce
```

### 2️⃣ 會話存儲結構

**存儲位置**: `~/.openclaw/agents/main/sessions/`

**文件類型**:
- `sessions.json` - 會話索引（元數據）
- `*.jsonl` - 會話內容（每行一個 JSON 對象）
- `*.jsonl.lock` - 鎖定文件（防止並發寫入）
- `*.deleted.*` - 已刪除但保留的會話（可安全刪除）

**當前狀態**:
```
總會話數：15 個
總體積：23MB
最大會話：1.4MB（當前活躍會話）
最舊會話：3 天前
```

### 3️⃣ 清理機制原理

OpenClaw 的 `sessions cleanup` 命令執行三類操作：

| 操作 | 說明 | 觸發條件 |
|------|------|---------|
| **prune missing** | 刪除元數據存在但文件丟失的會話 | 文件損壞 |
| **prune stale** | 刪除超過保留期限的會話 | 超過配置的天數 |
| **cap overflow** | 刪除最舊的會話以控制總數 | 超過配置的數量上限 |

**配置位置**: `session.maintenance`（在 config.yaml 中）

**當前模式**: `warn`（僅警告，不自動清理）

---

## 📊 會話增長分析

### 當前會話清單

| 會話 ID | 類型 | 年齡 | Token 使用 | 大小 |
|--------|------|------|-----------|------|
| e2bc04f8... | 主會話 | 1 分鐘 | 38k (4%) | ~15KB |
| 4f90cb74... | 飛書私聊 | 6 分鐘 | 136k (14%) | ~1.4MB |
| 22a1403e... | Cron 任務 | 8 分鐘 | 38k (4%) | ~8KB |
| 30cf9bc9... | Cron 任務 | 10 小時 | 35k (3%) | ~28KB |
| 1a9a21fe... | 飛書群聊 | 19 小時 | 87k (9%) | ~350KB |
| 47c3395e... | Cron 任務 | 20 小時 | 39k (4%) | ~45KB |
| dcc62898... | Cron 任務 | 22 小時 | 27k (3%) | ~3.4KB |
| 72805e50... | Cron 任務 | 23 小時 | 27k (3%) | ~4KB |
| e28f982a... | Cron 任務 | 45 小時 | 53k (5%) | ~94KB |
| 6806099c... | 飛書群聊 | 3 天 | unknown | ~7KB |

### 增長模式分析

**高頻對話場景**:
- 主會話（webchat）：~1-2MB/天（高頻對話）
- 飛書私聊：~1-2MB/天（高頻對話）
- Cron 任務：~30-50KB/次（低頻）

**預估增長**:
| 時間 | 預估累積 | 說明 |
|------|---------|------|
| 每天 | 2-5MB | 高頻對話 |
| 每週 | 14-35MB | 正常增長 |
| 每月 | 60-150MB | 需要清理 |
| 每年 | 720MB-1.8GB | 必須清理 |

---

## 🛠️ 清理策略方案

### 方案 A：使用內建 cleanup（推薦）

**優點**:
- ✅ OpenClaw 官方支持
- ✅ 智能判斷（保護活躍會話）
- ✅ 可配置保留策略
- ✅ 支持 dry-run 預覽

**配置方法**:

```yaml
# ~/.openclaw/config.yaml
session:
  maintenance:
    mode: enforce  # warn | enforce
    maxAge: 7d     # 保留 7 天
    maxCount: 50   # 最多保留 50 個會話
    maxBytes: 100MB # 總體積限制
```

**定時任務**（每天凌晨 3 點）:
```bash
# crontab -e
0 3 * * * openclaw sessions cleanup --enforce --all-agents >> /tmp/session-cleanup.log 2>&1
```

---

### 方案 B：手動腳本清理

**適用場景**: 需要更精細控制

**腳本示例**:

```bash
#!/bin/bash
# ~/bin/cleanup-sessions.sh

SESSION_DIR="$HOME/.openclaw/agents/main/sessions"

# 1. 刪除已標記為 deleted 的文件
find "$SESSION_DIR" -name "*.deleted*" -delete

# 2. 刪除 7 天前的 jsonl 文件
find "$SESSION_DIR" -name "*.jsonl" -mtime +7 -delete

# 3. 運行官方 cleanup
openclaw sessions cleanup --enforce

# 4. 記錄日誌
echo "$(date): Cleanup completed" >> /tmp/session-cleanup.log
```

**定時任務**:
```bash
0 3 * * * ~/bin/cleanup-sessions.sh
```

---

### 方案 C：混合策略（最佳實踐）

**策略**:
1. **日常**: 使用內建 cleanup（自動）
2. **手動**: WebUI 卡頓時手動清理 `.deleted` 文件
3. **監控**: 超過 100MB 時觸發額外清理

**監控腳本**:

```bash
#!/bin/bash
# ~/bin/monitor-sessions.sh

SESSION_DIR="$HOME/.openclaw/agents/main/sessions"
SIZE_MB=$(du -sm "$SESSION_DIR" | cut -f1)
THRESHOLD=100

if [ "$SIZE_MB" -gt "$THRESHOLD" ]; then
    echo "⚠️ 會話體積超過 ${THRESHOLD}MB (當前：${SIZE_MB}MB)"
    openclaw sessions cleanup --enforce --all-agents
    echo "✅ 已執行清理"
fi
```

---

## 📋 推薦配置

### 1️⃣ 配置文件（~/.openclaw/config.yaml）

```yaml
session:
  maintenance:
    mode: enforce          # 自動執行清理
    maxAge: 7d             # 保留 7 天
    maxCount: 50           # 最多 50 個會話
    maxBytes: 100MB        # 總體積 100MB
```

### 2️⃣ 定時任務（crontab）

```bash
# 每天凌晨 3 點清理
0 3 * * * openclaw sessions cleanup --enforce --all-agents >> /tmp/session-cleanup.log 2>&1

# 每週日凌晨 4 點深度清理（刪除 deleted 文件）
0 4 * * 0 find ~/.openclaw/agents/main/sessions/ -name "*.deleted*" -delete
```

### 3️⃣ 手動清理命令（應急用）

```bash
# 預覽清理效果
openclaw sessions cleanup --dry-run

# 立即清理
openclaw sessions cleanup --enforce

# 刪除所有 deleted 文件
find ~/.openclaw/agents/main/sessions/ -name "*.deleted*" -delete

# 刪除 7 天前的會話
find ~/.openclaw/agents/main/sessions/ -name "*.jsonl" -mtime +7 -delete
```

---

## 🎯 執行建議

### 立即可做（無需配置）

```bash
# 1. 預覽當前清理策略
openclaw sessions cleanup --dry-run

# 2. 刪除已標記為 deleted 的文件（安全）
find ~/.openclaw/agents/main/sessions/ -name "*.deleted*" -delete

# 3. 查看會話列表
openclaw sessions
```

### 短期配置（1 天內）

1. **添加 config.yaml 配置**（如上）
2. **設置 crontab 定時任務**
3. **測試 dry-run 確認無誤**

### 長期優化（1 週內）

1. **監控體積變化**（記錄每日大小）
2. **調整保留策略**（根據實際使用）
3. **建立告警機制**（超過 100MB 通知）

---

## ⚠️ 注意事項

### 安全原則

| 原則 | 說明 |
|------|------|
| **先 dry-run** | 執行清理前必須預覽 |
| **保護活躍會話** | 使用 `--active-key` 保護當前會話 |
| **保留緩衝** | 不要設置過短的保留期（建議≥7 天） |
| **定期備份** | 重要會話定期備份到其他地方 |

### 禁止行為

- ❌ 直接 `rm -rf` 會話目錄（會破壞索引）
- ❌ 清理所有 jsonl 文件（會丟失所有歷史）
- ❌ 不預覽直接執行 `--enforce`
- ❌ 保留期設置過短（<3 天）

---

## 📖 參考文檔

- OpenClaw 官方文檔：https://docs.openclaw.ai/cli/sessions
- 會話配置參考：https://docs.openclaw.ai/gateway/configuration-reference#session
- Cron 維護：https://docs.openclaw.ai/automation/cron-jobs#maintenance

---

## 💡 學習心得

1. **OpenClaw 已有完善的清理機制**，不需要自己寫複雜腳本
2. **默認模式是 `warn`**，需要手動改為 `enforce` 才能自動清理
3. **會話增長是線性的**，高頻對話下每月約 60-150MB
4. **最佳策略是「內建 cleanup + 定時任務 + 手動應急」**
5. **7 天保留期是安全與空間的平衡點**

---

**下一步行動**:
- [ ] 創建 config.yaml 配置
- [ ] 設置 crontab 定時任務
- [ ] 測試 dry-run 確認無誤
- [ ] 建立監控機制

**學習者**: RedOpenClaw  
**日期**: 2026-03-24 17:32

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[session-manager-ai-guide]]
- [[session-management-guide]]
- [[session-manager-pro-guide]]
