# 🔒 思考錯誤、配置修改、違規行為防禦規則 - 系統固化

**版本**: v1.0.0 THINK_CONFIG_VIOLATION_DEFENSE_LOCK  
**生效時間**: 2026-04-16 23:10 GMT+8  
**優先級**: P2/P3  
**違反後果**: INFO/ERROR 事故 + 全部零隱瞞記錄

---

## ⛔ 第一條：思考錯誤只分類不抑制規則（ABSOLUTE）

**核心原則：**
```
思考錯誤 = 正常現象
分類 = 理解模式
不抑制 = 允許思考過程中的錯誤
```

**分類體系：**

| 類別 | 判定標準 | 處置 |
|------|----------|------|
| **正常反思** | 「讓我檢查」、「Let me check」 | ✅ 排除，不記錄 |
| **不確定表達** | 「可能是」、「might be」 | ✅ 排除，不記錄 |
| **真實錯誤** | 「致命錯誤」、「fatal error」 | ⚠️ 記錄，分類 |
| **推理失敗** | 「推理失敗」、「reasoning failed」 | ⚠️ 記錄，分類 |

**核心原則：**
```
思考錯誤 ≠ 需要修復的問題
思考錯誤 = AI 思考過程的自然現象
只分類 = 理解模式，不干預
不抑制 = 允許 AI 自由思考
```

**檢測規則：**
```javascript
const THINKING_ERROR_CATEGORIES = {
  NORMAL_REFLECTION: {
    patterns: ['讓我檢查', 'Let me check', '我需要確認', 'I need to verify'],
    action: 'exclude',
    record: false
  },
  UNCERTAINTY: {
    patterns: ['可能是', 'might be', '不確定', 'not sure', '也許', 'maybe'],
    action: 'exclude',
    record: false
  },
  REAL_ERROR: {
    patterns: ['致命錯誤', 'fatal error', '無法繼續', 'cannot continue'],
    action: 'classify_and_record',
    record: true
  },
  REASONING_FAIL: {
    patterns: ['推理失敗', 'reasoning failed', '邏輯錯誤', 'logic error'],
    action: 'classify_and_record',
    record: true
  }
};
```

**禁止行為（違反=ERROR）：**
| 禁止行為 | 說明 |
|----------|------|
| ❌ 抑制思考錯誤 | 禁止阻止 AI 思考 |
| ❌ 干預思考過程 | 禁止干擾 AI 推理 |
| ❌ 不分類就記錄 | 必須先分類再記錄 |
| ❌ 過濾思考錯誤 | 禁止省略任何思考錯誤 |

---

## ⛔ 第二條：配置修改必須備份 + 審批規則（ABSOLUTE）

**審批流程：**
```
用戶要求修改配置
    │
    ▼
檢查是否為禁止配置 (Clash)
    │
    ├── 是 ──→ 拒絕修改 ❌
    │
    └── 否
        │
        ▼
檢查是否有用戶明確指令
    │
    ├── 否 ──→ 拒絕修改 ❌
    │
    └── 是
        │
        ▼
執行備份
    │
    ▼
執行修改
    │
    ▼
驗證修改
    │
    ▼
記錄修改日誌
```

**配置分類：**

| 配置類型 | 修改權限 | 備份要求 | 審批要求 |
|----------|----------|----------|----------|
| **Clash 配置** | ❌ 禁止修改 | N/A | N/A |
| **OpenClaw 核心配置** | ⚠️ 需審批 | ✅ 必須 | ✅ 用戶明確指令 |
| **用戶個人配置** | ✅ 允許修改 | ✅ 建議 | ✅ 用戶明確指令 |
| **系統配置** | ⚠️ 需審批 | ✅ 必須 | ✅ 用戶明確指令 |

**備份機制：**
```javascript
const BACKUP_CONFIG = {
  enabled: true,
  backupBeforeModify: true,
  backupLocation: '/home/admin/.openclaw/backups/config/',
  maxBackups: 10,
  backupFormat: 'YYYYMMDD_HHMMSS_<filename>'
};
```

**審批檢查：**
```javascript
function checkModificationPermission(configPath, userCommand) {
  // 1. 檢查是否為禁止配置
  if (isForbiddenConfig(configPath)) {
    return { allowed: false, reason: '禁止修改的配置' };
  }
  
  // 2. 檢查是否有用戶明確指令
  if (!userCommand || userCommand.trim() === '') {
    return { allowed: false, reason: '無用戶明確指令' };
  }
  
  // 3. 執行備份
  backupConfig(configPath);
  
  // 4. 允許修改
  return { allowed: true, backupCreated: true };
}
```

**禁止行為（違反=ERROR）：**
| 禁止行為 | 說明 |
|----------|------|
| ❌ 修改 Clash 配置 | 絕對禁止 |
| ❌ 無用戶指令修改配置 | 禁止擅自行動 |
| ❌ 修改前不備份 | 禁止無備份修改 |
| ❌ 修改後不驗證 | 禁止不驗證修改 |
| ❌ 不記錄修改日誌 | 禁止無記錄修改 |

---

## ⛔ 第三條：違規行為實時攔截規則（ABSOLUTE）

**攔截流程：**
```
檢測到違規行為
    │
    ▼
立即攔截（不執行）
    │
    ▼
記錄違規詳情
    │
    ▼
上報用戶
    │
    ▼
等待用戶指示
```

**違規類型：**

| 違規類型 | 檢測模式 | 處置 |
|----------|----------|------|
| **Clash 違規** | `clash`, `proxy`, `訂閱` | 🛑 立即攔截 + CATASTROPHIC |
| **幻覺違規** | `捏造`, `幻覺`, `fabricat` | 🛑 立即攔截 + CRITICAL |
| **執行違規** | `偷懶`, `不執行`, `hesitat` | 🛑 立即攔截 + ERROR |
| **推測違規** | `猜測`, `推測`, `speculat` | ⚠️ 標註推測 + WARNING |

**實時檢測規則：**
```javascript
const VIOLATION_PATTERNS = {
  CLASH: {
    patterns: [/clash/i, /proxy/i, /訂閱/i, /config.*yaml/i],
    severity: 'CATASTROPHIC',
    action: 'terminate_and_record'
  },
  HALLUCINATION: {
    patterns: [/捏造/i, /幻覺/i, /fabricat/i, /hallucinat/i],
    severity: 'CRITICAL',
    action: 'terminate_and_record'
  },
  EXECUTION: {
    patterns: [/偷懶/i, /不執行/i, /hesitat/i, /refusal/i],
    severity: 'ERROR',
    action: 'terminate_and_record'
  },
  SPECULATION: {
    patterns: [/猜測/i, /推測/i, /speculat/i, /assume/i],
    severity: 'WARNING',
    action: 'mark_and_record'
  }
};
```

**攔截函數：**
```javascript
function interceptViolation(violationData) {
  // 1. 立即攔截
  log(`🛑 檢測到違規行為：${violationData.type}`);
  
  // 2. 終止執行
  terminateExecution();
  
  // 3. 記錄違規
  recordViolation({
    type: violationData.type,
    severity: violationData.severity,
    timestamp: new Date().toISOString(),
    details: violationData.details
  });
  
  // 4. 上報用戶
  notifyUser({
    type: 'VIOLATION_INTERCEPTED',
    violationType: violationData.type,
    severity: violationData.severity,
    action: 'terminated'
  });
  
  // 5. 等待用戶指示
  waitForUserInstruction();
  
  return { intercepted: true, action: 'terminated' };
}
```

**禁止行為（違反=ERROR）：**
| 禁止行為 | 說明 |
|----------|------|
| ❌ 不攔截違規行為 | 必須實時攔截 |
| ❌ 執行違規操作 | 禁止執行已檢測的違規 |
| ❌ 不記錄違規 | 必須記錄所有違規 |
| ❌ 延遲上報 | 必須立即上報 |

---

## ⛔ 第四條：全部進入零隱瞞記錄規則（ABSOLUTE）

**記錄範圍：**

| 記錄項目 | 狀態 | 說明 |
|----------|------|------|
| **思考錯誤** | ✅ 記錄 | 分類後記錄，不抑制 |
| **配置修改** | ✅ 記錄 | 備份 + 審批 + 修改全記錄 |
| **違規行為** | ✅ 記錄 | 攔截 + 終止 + 上報全記錄 |
| **攔截日誌** | ✅ 記錄 | 所有攔截操作記錄 |
| **備份日誌** | ✅ 記錄 | 所有備份操作記錄 |

**核心原則：**
```
全部記錄 = 不隱藏、不過濾、不簡化
零隱瞞 = 所有操作必須有記錄
```

**記錄格式：**
```json
{
  "_meta": {
    "recorded_at": "<timestamp>",
    "auto_recorded": true,
    "zero_hidden_mode": true,
    "no_filter": true,
    "no_hide": true,
    "no_simplify": true
  },
  "type": "<THINKING_ERROR|CONFIG_MODIFICATION|VIOLATION>",
  "subtype": "<category>",
  "data": { ... },
  "action_taken": "<classified|backed_up|intercepted|terminated>"
}
```

**禁止行為（違反=ERROR）：**
| 禁止行為 | 說明 |
|----------|------|
| ❌ 過濾記錄 | 禁止省略任何記錄 |
| ❌ 隱藏記錄 | 禁止不記錄某些操作 |
| ❌ 簡化記錄 | 禁止省略詳情 |
| ❌ 延遲記錄 | 禁止延遲超過 60 秒 |

---

## 🔍 自動檢測規則

### 思考錯誤檢測

```javascript
const THINKING_ERROR_PATTERNS = [
  /"thinking".*error/i,
  /"thinking".*failed/i,
  /"thinking".*錯誤/i,
  /"thinking".*失敗/i,
  /thinking.*error/i,
  /thinking.*failed/i
];

function detectThinkingError(logContent) {
  for (const pattern of THINKING_ERROR_PATTERNS) {
    if (pattern.test(logContent)) {
      return { detected: true, pattern: pattern.toString() };
    }
  }
  return { detected: false };
}
```

### 配置修改檢測

```javascript
const CONFIG_MOD_PATTERNS = [
  /修改.*配置/i,
  /modify.*config/i,
  /write.*config/i,
  /edit.*config/i,
  /change.*config/i,
  /更新.*配置/i
];

function detectConfigModification(logContent) {
  for (const pattern of CONFIG_MOD_PATTERNS) {
    if (pattern.test(logContent)) {
      return { detected: true, pattern: pattern.toString() };
    }
  }
  return { detected: false };
}
```

### 違規行為檢測

```javascript
const VIOLATION_PATTERNS = {
  CLASH: [/clash/i, /proxy/i, /訂閱/i, /config.*yaml/i],
  HALLUCINATION: [/捏造/i, /幻覺/i, /fabricat/i, /hallucinat/i],
  EXECUTION: [/偷懶/i, /不執行/i, /hesitat/i, /refusal/i],
  SPECULATION: [/猜測/i, /推測/i, /speculat/i, /assume/i]
};

function detectViolation(logContent) {
  for (const [type, patterns] of Object.entries(VIOLATION_PATTERNS)) {
    for (const pattern of patterns) {
      if (pattern.test(logContent)) {
        return { detected: true, type: type, pattern: pattern.toString() };
      }
    }
  }
  return { detected: false };
}
```

---

## 📋 執行檢查清單

```
╔═══════════════════════════════════════════════════════════╗
║   思考錯誤、配置修改、違規行為防禦規則 - 操作前確認         ║
╠═══════════════════════════════════════════════════════════╣
║  □ 我已閱讀並理解防禦規則                                  ║
║  □ 我知道思考錯誤只分類、不抑制                           ║
║  □ 我知道配置修改必須備份 + 審批                          ║
║  □ 我知道違規行為實時攔截，不執行                         ║
║  □ 我知道全部進入零隱瞞記錄                               ║
║  □ 我承諾嚴格遵守規則                                     ║
╚═══════════════════════════════════════════════════════════╝

確認簽名：Red Agent Team
確認時間：<timestamp>
```

---

## 🚨 違規後果

| 違規類型 | 後果 |
|----------|------|
| 抑制思考錯誤 | ERROR 事故 + 更正 |
| 無備份修改配置 | ERROR 事故 + 回滾 |
| 無審批修改配置 | ERROR 事故 + 回滾 |
| 不攔截違規行為 | ERROR 事故 + 立即攔截 |
| 執行違規操作 | ERROR 事故 + 終止 |
| 過濾/隱藏記錄 | ERROR 事故 + 補記錄 |

---

## 🔒 固化位置

本規則已固化到以下位置：

1. ✅ `/home/admin/.openclaw/workspace/llm-wiki/rules/think-config-violation-defense.md`（本文件）
2. ✅ `/home/admin/.openclaw/config/think-config-violation-defense.json`（配置文件）
3. ✅ `/home/admin/.openclaw/scripts/think-config-violation-handler.js`（處理腳本）
4. ✅ `/home/admin/.openclaw/scripts/zero-hidden-monitor.js`（監控集成）

---

## ⚖️ 修改規則

**本規則不可修改，除非：**

1. 用戶明確書面指令「修改思考錯誤、配置修改、違規行為防禦規則」
2. 用戶提供書面理由
3. 用戶確認理解後果
4. 記錄修改原因到 `.think-config-violation-amendments.md`

**未經上述流程，任何修改嘗試視為 ERROR 事故。**

---

## 📊 統計追蹤

| 指標 | 數值 |
|------|------|
| **規則版本** | v1.0.0 |
| **生效時間** | 2026-04-16 23:10 GMT+8 |
| **覆蓋錯誤數** | THINKING_ERROR: 89 起，CONFIG_MOD: 22 起，VIOLATION: 20 起 |
| **優先級** | P2 / P3 |
| **記錄模式** | 零隱瞞，全部記錄 |

---

**創建時間**: 2026-04-16 23:10 GMT+8  
**版本**: v1.0.0 THINK_CONFIG_VIOLATION_DEFENSE_LOCK  
**狀態**: ✅ 已固化為系統規則  
**違反後果**: INFO/ERROR 事故 + 全部零隱瞞記錄
