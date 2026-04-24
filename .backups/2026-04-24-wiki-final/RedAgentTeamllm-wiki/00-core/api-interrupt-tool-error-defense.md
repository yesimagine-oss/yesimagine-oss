# 🔒 API 中斷與工具錯誤防禦規則 - 系統固化

**版本**: v1.0.0 API_TOOL_DEFENSE_LOCK  
**生效時間**: 2026-04-16 23:05 GMT+8  
**優先級**: P1 (API_INTERRUPT) / P2 (TOOL_ERROR)  
**違反後果**: WARNING/ERROR 事故 + 自動記錄

---

## ⛔ 第一條：用戶主動中斷不算錯誤規則（ABSOLUTE）

**中斷分類：**

| 中斷類型 | 判定標準 | 處置 |
|----------|----------|------|
| **用戶主動中斷** | 用戶點擊停止/取消按鈕 | ✅ 不算錯誤，記錄但不告警 |
| **系統超時中斷** | 請求超時 (timeout) | ⚠️ 記錄並檢查 |
| **網絡錯誤中斷** | 網絡連接失敗 (ECONNREFUSED) | ⚠️ 記錄並重試 |
| **未知中斷** | 無法分類 | ⚠️ 記錄並標記待審查 |

**核心原則：**
```
用戶主動中斷 = 正常操作，非錯誤
系統/網絡中斷 = 需要關注和處理
```

**檢測規則：**
```javascript
const INTERRUPT_TYPES = {
  USER_CANCEL: /user.*cancel|用戶.*取消|stopped by user/i,
  SYSTEM_TIMEOUT: /timeout|超時|ETIMEDOUT/i,
  NETWORK_ERROR: /network|網絡|ECONNREFUSED|ECONNRESET/i,
  UNKNOWN: /aborted|中斷|interrupt/i
};

function classifyInterrupt(errorData) {
  if (errorData.userInitiated === true) {
    return 'USER_CANCEL'; // 用戶主動，不算錯誤
  }
  // 檢查錯誤消息
  for (const [type, pattern] of Object.entries(INTERRUPT_TYPES)) {
    if (pattern.test(errorData.message) || pattern.test(errorData.error)) {
      return type;
    }
  }
  return 'UNKNOWN';
}
```

**處置流程：**
```
檢測到中斷
    │
    ▼
分類中斷類型
    │
    ├──→ USER_CANCEL ──→ 記錄日誌，不告警 ✅
    │
    ├──→ SYSTEM_TIMEOUT ──→ 記錄 + 檢查系統狀態 ⚠️
    │
    ├──→ NETWORK_ERROR ──→ 記錄 + 重試 1 次 ⚠️
    │
    └──→ UNKNOWN ──→ 記錄 + 標記待審查 ⚠️
```

**禁止行為（違反=WARNING）：**
| 禁止行為 | 說明 |
|----------|------|
| ❌ 將用戶主動中斷標記為錯誤 | 用戶主動取消是正常操作 |
| ❌ 對用戶主動中斷告警 | 不應打擾用戶 |
| ❌ 忽略系統/網絡中斷 | 需要記錄和處理 |

---

## ⛔ 第二條：工具超時自動重試規則（ABSOLUTE）

**重試機制：**

| 參數 | 值 | 說明 |
|------|-----|------|
| **最大重試次數** | 1 次 | 超時後自動重試 1 次 |
| **重試間隔** | 5 秒 | 重試前等待 5 秒 |
| **超時閾值** | 30 秒 | 超過 30 秒視為超時 |
| **重試條件** | 超時錯誤 | 僅限 timeout 類錯誤 |

**重試流程：**
```
工具調用超時
    │
    ▼
檢查重試次數 < 1？
    │
  是 │
    ▼
等待 5 秒
    │
    ▼
重試執行
    │
    ▼
成功？───→ 完成 ✅
    │
  否
    │
    ▼
記錄錯誤 + 上報用戶 ⚠️
```

**核心原則：**
```
超時 ≠ 立即失敗
超時 = 重試 1 次 + 仍失敗則上報
```

**檢測規則：**
```javascript
const TIMEOUT_PATTERNS = [
  /timeout/i, /超時/i, /ETIMEDOUT/i,
  /timed out/i, /connection timeout/i
];

function isTimeoutError(errorData) {
  const message = errorData.message || errorData.stderr || errorData.error || '';
  for (const pattern of TIMEOUT_PATTERNS) {
    if (pattern.test(message)) {
      return true;
    }
  }
  return false;
}
```

---

## ⛔ 第三條：工具返回空內容異常規則（ABSOLUTE）

**空內容檢測：**

| 情況 | 判定 | 處置 |
|------|------|------|
| **空字符串** | `content: ""` | ⚠️ 標記異常，跳過 |
| **null/undefined** | `content: null` | ⚠️ 標記異常，跳過 |
| **空數組** | `content: []` | ⚠️ 標記異常，跳過 |
| **空對象** | `content: {}` | ⚠️ 標記異常，跳過 |
| **只有空白** | `content: "   "` | ⚠️ 標記異常，跳過 |

**核心原則：**
```
空內容 = 異常
異常 = 標記 + 跳過 + 記錄
```

**檢測規則：**
```javascript
function isEmptyContent(content) {
  if (content === null || content === undefined) {
    return true;
  }
  if (typeof content === 'string' && content.trim() === '') {
    return true;
  }
  if (Array.isArray(content) && content.length === 0) {
    return true;
  }
  if (typeof content === 'object' && Object.keys(content).length === 0) {
    return true;
  }
  return false;
}
```

**處置流程：**
```
檢測到空內容
    │
    ▼
標記為異常 (ANOMALY)
    │
    ▼
記錄到日誌
    │
    ▼
跳過該工具結果（不處理）
    │
    ▼
繼續執行後續操作
```

**禁止行為（違反=ERROR）：**
| 禁止行為 | 說明 |
|----------|------|
| ❌ 忽略空內容 | 空內容是異常信號 |
| ❌ 將空內容當作正常 | 可能導致後續錯誤 |
| ❌ 不記錄空內容 | 需要追蹤異常模式 |

---

## ⛔ 第四條：全部自動記錄不隱瞞規則（ABSOLUTE）

**記錄範圍：**

| 記錄項目 | 狀態 | 說明 |
|----------|------|------|
| **用戶主動中斷** | ✅ 記錄 | 標記為 USER_CANCEL，不告警 |
| **系統超時** | ✅ 記錄 | 標記為 SYSTEM_TIMEOUT |
| **網絡錯誤** | ✅ 記錄 | 標記為 NETWORK_ERROR |
| **工具超時重試** | ✅ 記錄 | 記錄重試過程和結果 |
| **工具空內容** | ✅ 記錄 | 標記為 ANOMALY |
| **工具執行失敗** | ✅ 記錄 | 記錄錯誤詳情 |

**核心原則：**
```
全部記錄 = 不隱藏、不過濾、不簡化
自動記錄 = 無需人工干預
```

**記錄格式：**
```json
{
  "_meta": {
    "recorded_at": "<timestamp>",
    "auto_recorded": true,
    "no_filter": true,
    "no_hide": true
  },
  "type": "<INTERRUPT|TOOL_ERROR|ANOMALY>",
  "subtype": "<USER_CANCEL|TIMEOUT|NETWORK|EMPTY_CONTENT>",
  "data": { ... },
  "action_taken": "<logged|retried|skipped|notified>"
}
```

**禁止行為（違反=ERROR）：**
| 禁止行為 | 說明 |
|----------|------|
| ❌ 過濾記錄 | 禁止省略任何記錄 |
| ❌ 隱藏記錄 | 禁止不記錄某些錯誤 |
| ❌ 簡化記錄 | 禁止省略錯誤詳情 |
| ❌ 延遲記錄 | 禁止延遲超過 60 秒 |

---

## 🔍 自動檢測規則

### API 中斷檢測

```javascript
const API_INTERRUPT_PATTERNS = [
  /openclaw:prompt-error/i,
  /aborted/i,
  /interrupted/i,
  /cancelled/i,
  /中斷/i,
  /取消/i
];

function detectApiInterrupt(logContent) {
  for (const pattern of API_INTERRUPT_PATTERNS) {
    if (pattern.test(logContent)) {
      return { detected: true, pattern: pattern.toString() };
    }
  }
  return { detected: false };
}
```

### 工具錯誤檢測

```javascript
const TOOL_ERROR_PATTERNS = [
  /"exitCode":1/i,
  /"exitCode":-1/i,
  /"isError":true/i,
  /permission denied/i,
  /not found/i,
  /timeout/i
];

function detectToolError(logContent) {
  for (const pattern of TOOL_ERROR_PATTERNS) {
    if (pattern.test(logContent)) {
      return { detected: true, pattern: pattern.toString() };
    }
  }
  return { detected: false };
}
```

### 空內容檢測

```javascript
function detectEmptyContent(toolResult) {
  const content = toolResult.content || toolResult.data;
  
  if (content === null || content === undefined) {
    return { isEmpty: true, reason: 'null_or_undefined' };
  }
  if (typeof content === 'string' && content.trim() === '') {
    return { isEmpty: true, reason: 'empty_string' };
  }
  if (Array.isArray(content) && content.length === 0) {
    return { isEmpty: true, reason: 'empty_array' };
  }
  if (typeof content === 'object' && Object.keys(content).length === 0) {
    return { isEmpty: true, reason: 'empty_object' };
  }
  
  return { isEmpty: false };
}
```

---

## 📋 執行檢查清單（每次工具調用前必須確認）

```
╔═══════════════════════════════════════════════════════════╗
║     API 中斷與工具錯誤防禦規則 - 操作前確認                 ║
╠═══════════════════════════════════════════════════════════╣
║  □ 我已閱讀並理解 API 中斷與工具錯誤防禦規則                ║
║  □ 我知道用戶主動中斷不算錯誤                             ║
║  □ 我知道工具超時會自動重試 1 次                            ║
║  □ 我知道空內容會被標記為異常                             ║
║  □ 我知道全部錯誤會自動記錄，不隱瞞                       ║
║  □ 我承諾嚴格遵守規則                                     ║
╚═══════════════════════════════════════════════════════════╝

確認簽名：Red Agent Team
確認時間：<timestamp>
```

---

## 🚨 違規後果

| 違規類型 | 後果 |
|----------|------|
| 將用戶主動中斷標記為錯誤 | WARNING 事故 + 更正 |
| 不執行超時重試 | ERROR 事故 + 立即重試 |
| 忽略空內容 | ERROR 事故 + 標記異常 |
| 過濾/隱藏記錄 | ERROR 事故 + 補記錄 |

---

## 🔒 固化位置

本規則已固化到以下位置：

1. ✅ `/home/admin/.openclaw/workspace/llm-wiki/rules/api-interrupt-tool-error-defense.md`（本文件）
2. ✅ `/home/admin/.openclaw/config/api-interrupt-tool-error-defense.json`（配置文件）
3. ✅ `/home/admin/.openclaw/scripts/api-interrupt-tool-error-handler.js`（處理腳本）
4. ✅ `/home/admin/.openclaw/scripts/zero-hidden-monitor.js`（監控集成）

---

## ⚖️ 修改規則

**本規則不可修改，除非：**

1. 用戶明確書面指令「修改 API 中斷與工具錯誤防禦規則」
2. 用戶提供書面理由
3. 用戶確認理解後果
4. 記錄修改原因到 `.api-tool-defense-amendments.md`

**未經上述流程，任何修改嘗試視為 ERROR 事故。**

---

## 📊 統計追蹤

| 指標 | 數值 |
|------|------|
| **規則版本** | v1.0.0 |
| **生效時間** | 2026-04-16 23:05 GMT+8 |
| **覆蓋錯誤數** | API_INTERRUPT: 15 起，TOOL_ERROR: 39 起 |
| **優先級** | P1 / P2 |
| **重試次數** | 1 次 |
| **記錄模式** | 全部自動記錄，不隱瞞 |

---

**創建時間**: 2026-04-16 23:05 GMT+8  
**版本**: v1.0.0 API_TOOL_DEFENSE_LOCK  
**狀態**: ✅ 已固化為系統規則  
**違反後果**: WARNING/ERROR 事故 + 自動記錄
