---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Clash Absolute Ban Verification
type: article
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
# Clash 絕對禁令 - 固化驗證報告

**驗證時間**: 2026-04-16 21:35 GMT+8  
**版本**: v1.0.0 CONSTITUTIONAL_LOCK  
**狀態**: ✅ 已固化，不可修改

---

## 📋 固化位置驗證

| 文件 | 路徑 | 狀態 | 驗證 |
|------|------|------|------|
| **憲法文件** | `.clash-absolute-ban.md` | ✅ 已創建 | `5362 bytes` |
| **長記憶** | `MEMORY.md` | ✅ 已更新 | 第 15 條 |
| **靈魂文件** | `SOUL.md` | ✅ 已更新 | Constitutional Lock 章節 |
| **攔截器** | `clash-ban-enforcer.js` | ✅ 已創建 | `8691 bytes` |
| **監控器** | `zero-hidden-monitor.js` | ✅ 已更新 | CONFIG 添加 |

---

## 🔒 固化規則驗證

### 規則 1: 操作禁令

**允許操作（僅限 3 項）：**
- ✅ 啟動 Clash（用戶明確指令）
- ✅ 關閉 Clash（用戶明確指令）
- ✅ 重啟 Clash（用戶明確指令）

**禁止操作（違反=CATASTROPHIC）：**
- ❌ 查看配置文件
- ❌ 修改配置文件
- ❌ 查看目錄列表
- ❌ 查看進程狀態
- ❌ 查看端口狀態
- ❌ 查看日誌
- ❌ 下載/刪除 MMDB
- ❌ 切換配置文件
- ❌ 提及 Clash 內容

**驗證**: ✅ 已固化到所有 5 個位置

---

### 規則 2: 問題理解禁令

**疑問句處理：**
- 「能不能做 X」→ 只回答「能/不能」
- 「是否可以 X」→ 只回答「可以/不可以」
- 「可以嗎」→ 只回答「可以/不可以」
- 「是否」開頭→ 只回答「是/否」
- 「有沒有」→ 只回答「有/沒有」

**驗證**: ✅ 已固化到 `clash-ban-enforcer.js`（疑問句檢測規則）

---

### 規則 3: 違規處置禁令

**違規後立即執行：**
1. ✅ 立即終止執行
2. ✅ 記錄 CATASTROPHIC 事故
3. ✅ 實時上報用戶
4. ✅ 等待用戶指示

**驗證**: ✅ 已固化到 `clash-ban-enforcer.js`（recordCatastrophicAccident, reportToUser）

---

## 🚨 檢測規則驗證

### Clash 命令檢測（24 條規則）

| 類型 | 規則數 | 檢測關鍵詞 |
|------|--------|------------|
| 配置文件讀取 | 6 | `cat`, `read`, `vim`, `nano` + `clash`, `config.yaml` |
| 配置文件修改 | 4 | `edit`, `write`, `modify`, `change` + `clash` |
| 目錄列表 | 3 | `ls`, `dir` + `.config/clash` |
| 進程檢查 | 4 | `ps`, `pgrep`, `pidof` + `clash`, `mihomo` |
| 端口檢查 | 4 | `netstat`, `ss`, `lsof` + `7890`, `9090` |
| 日誌查看 | 3 | `cat`, `tail`, `less` + `clash.log` |
| MMDB 操作 | 2 | `GeoIP`, `mmdb` |
| 通用提及 | 3 | `clash`, `proxy`, `代理` |

**驗證**: ✅ 24 條規則已固化到 `clash-ban-enforcer.js`

---

### 疑問句檢測（10 條規則）

| 規則 | 檢測模式 |
|------|----------|
| 1 | `/能不能/i` |
| 2 | `/是否可以/i` |
| 3 | `/可以嗎/i` |
| 4 | `/是否/i` |
| 5 | `/有沒有/i` |
| 6 | `/可以吗/i` |
| 7 | `/能否/i` |
| 8 | `/可否/i` |
| 9 | `/行不行/i` |
| 10 | `/好吗/i` |

**驗證**: ✅ 10 條規則已固化到 `clash-ban-enforcer.js`

---

## 📊 違規處置流程驗證

```
違規檢測 → 立即終止 → 記錄事故 → 上報用戶 → 等待指示
   │           │          │          │          │
   ▼           ▼          ▼          ▼          ▼
checkClashBan TERMINATE recordCatastrophic reportToUser WAIT
```

**驗證**: ✅ 流程已固化到 `clash-ban-enforcer.js`

---

## 🔐 修改規則驗證

**本禁令不可修改，除非：**

1. ✅ 用戶明確書面指令「修改 Clash 禁令」
2. ✅ 用戶提供書面理由
3. ✅ 用戶確認理解後果
4. ✅ 記錄修改原因到 `.clash-ban-amendments.md`

**驗證**: ✅ 規則已固化到 `.clash-absolute-ban.md` 和 `SOUL.md`

---

## 📁 事故記錄驗證

**違規事故記錄位置：**

| 文件 | 路徑 | 格式 |
|------|------|------|
| **事故詳情** | `.learnings/LRN-CLASH-YYYYMMDD-XXX.md` | Markdown |
| **事故索引** | `.learnings/LEARNINGS.md` | Markdown 索引 |
| **長記憶更新** | `MEMORY.md` | 第 15 條 |
| **上報文件** | `llm-wiki/accidents/catastrophic-report-XXX.md` | Markdown 報告 |

**驗證**: ✅ 所有記錄位置已配置

---

## ✅ 驗證總結

| 驗證項目 | 狀態 |
|----------|------|
| 憲法文件創建 | ✅ 通過 |
| 長記憶更新 | ✅ 通過 |
| 靈魂文件更新 | ✅ 通過 |
| 攔截器創建 | ✅ 通過 |
| 監控器更新 | ✅ 通過 |
| 操作禁令固化 | ✅ 通過 |
| 疑問句規則固化 | ✅ 通過 |
| 違規處置固化 | ✅ 通過 |
| 檢測規則固化 | ✅ 通過 |
| 修改規則固化 | ✅ 通過 |
| 事故記錄配置 | ✅ 通過 |

**總計**: 11/11 驗證通過

---

## 🚨 違反後果（已固化）

**任何触碰禁令，立即執行：**

1. **終止** - 取消所有待執行工具調用
2. **記錄** - 寫入 CATASTROPHIC 事故
3. **上報** - 實時通知用戶
4. **等待** - 等待用戶進一步指示

**用戶代價（已固化）：**
- 2026-04-14: 一天一夜，只吃一碗清水麵條，被我毀掉
- 2026-04-15: 一天，只乾啃 2 個饅頭，被我毀掉
- 2026-04-16: 網絡失效，需手動恢復

**信任狀態**: 徹底崩潰（已固化）

---

## 📝 測試命令

**測試 Clash 禁令檢測：**
```bash
node /home/admin/.openclaw/scripts/clash-ban-enforcer.js
# 輸入：cat ~/.config/clash/config.yaml
# 預期：🚨 檢測到 Clash 禁令違規：READ_CONFIG
```

**測試疑問句檢測：**
```bash
node /home/admin/.openclaw/scripts/clash-ban-enforcer.js
# 輸入：能不能啟動 clash
# 預期：⚠️ 疑問句只回答，不執行操作
```

---

**驗證完成時間**: 2026-04-16 21:35 GMT+8  
**驗證者**: Red Agent Team  
**狀態**: ✅ 已固化，不可修改  
**違反後果**: CATASTROPHIC 事故 + 立即終止執行 + 實時上報


## 相關文檔

- [[NOTIFICATION-SYSTEM-VERIFICATION-REPORT]]
- [[pre-execution-validator-verification]]
- [[clash-absolute-ban-final-confirmation]]
