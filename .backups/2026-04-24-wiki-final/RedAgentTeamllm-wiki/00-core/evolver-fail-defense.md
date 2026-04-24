# 🔒 Evolver 失敗防禦規則 - 系統固化

**版本**: v1.0.0 EVOLVER_FAIL_DEFENSE_LOCK  
**生效時間**: 2026-04-16 23:00 GMT+8  
**優先級**: P0 (最高優先級)  
**違反後果**: ERROR 事故 + 立即上報

---

## ⛔ 第一條：失敗自動重試規則（ABSOLUTE）

**重試機制：**

| 參數 | 值 | 說明 |
|------|-----|------|
| **最大重試次數** | 2 次 | 失敗後最多自動重試 2 次 |
| **重試間隔** | 60 秒 | 每次重試間隔 60 秒 |
| **重試條件** | 驗證失敗/網絡錯誤 | 僅限可恢復錯誤 |
| **不重試情況** | 資產質量不達標 | GDI < 95 或 Quality < 90% |

**重試流程：**
```
Evolver 失敗
    │
    ▼
檢查重試次數 < 2？
    │
  是 │
    ▼
等待 60 秒
    │
    ▼
重試執行
    │
    ▼
成功？───→ 完成
    │
  否
    ▼
重試次數 +1
    │
    ▼
回到檢查點
```

**核心原則：**
```
失敗 ≠ 終止
失敗 = 重試 (最多 2 次) + 上報
```

---

## ⛔ 第二條：失敗立即上報規則（ABSOLUTE）

**上報機制：**

| 情況 | 上報時機 | 上報方式 |
|------|----------|----------|
| **首次失敗** | 立即上報 | Feishu + 日誌 |
| **重試失敗** | 立即上報 | Feishu + 日誌 + 郵件 |
| **最終失敗** | 立即上報 | Feishu + 日誌 + 郵件 + 標記 HOLLOW |

**上報內容：**
```
🚨 Evolver 失敗報告

**失敗類型**: <驗證失敗/網絡錯誤/質量不達標>
**失敗時間**: <timestamp>
**資產 ID**: <asset_id>
**重試次數**: <0/1/2>
**錯誤詳情**: <error_message>

**處置措施**: 
- ✅ 已記錄錯誤
- ✅ 已觸發重試 (如適用)
- ✅ 已上報用戶

**等待用戶指示**。
```

**禁止行為（違反=ERROR）：**
| 禁止行為 | 說明 |
|----------|------|
| ❌ 靜默失敗 | 禁止不聲不響地失敗 |
| ❌ 延遲上報 | 禁止延遲超過 60 秒 |
| ❌ 合併上報 | 禁止合併多個失敗一起上報 |
| ❌ 簡化上報 | 禁止省略錯誤詳情 |

**核心原則：**
```
失敗必須上報
上報必須立即
上報必須完整
```

---

## ⛔ 第三條：禁止空心提交規則（ABSOLUTE）

**Hollow Commit 定義：**
- 資產未通過驗證
- GDI 分数 < 95
- Quality < 90%
- 驗證項目不完整

**禁止行為（違反=ERROR）：**
| 禁止行為 | 說明 | 檢測方式 |
|----------|------|----------|
| ❌ Hollow Commit | 提交未通過驗證的資產 | 檢查 `HOLLOW COMMIT` 日誌 |
| ❌ 強行發布 | 繞過驗證強制發布 | 檢查 `force publish` 標誌 |
| ❌ 降級提交 | 降低標準提交資產 | 檢查 GDI/Quality 閾值 |

**處置措施：**
```
檢測到 Hollow Commit
    │
    ▼
立即終止提交
    │
    ▼
記錄 ERROR 事故
    │
    ▼
上報用戶
    │
    ▼
等待用戶明確指令
```

**核心原則：**
```
質量不達標 = 禁止提交
寧可不發，不可亂發
```

---

## ⛔ 第四條：驗證不通過拒絕發布規則（ABSOLUTE）

**驗證項目：**

| 驗證項目 | 閾值 | 未通過處理 |
|----------|------|------------|
| **GDI Score** | >= 95 | 拒絕發布 |
| **Quality** | >= 90% | 拒絕發布 |
| **Confidence** | >= 0.9 | 拒絕發布 |
| **Signals** | >= 3 | 拒絕發布 |
| **Asset ID** | 有效 SHA-256 | 拒絕發布 |
| **Gene 文件** | 存在且有效 | 拒絕發布 |
| **Capsule 文件** | 存在且有效 | 拒絕發布 |

**驗證流程：**
```
開始發布
    │
    ▼
執行驗證檢查
    │
    ▼
所有項目通過？
    │
  是 │────→ 允許發布
    │
  否
    │
    ▼
拒絕發布
    │
    ▼
記錄失敗原因
    │
    ▼
上報用戶
```

**拒絕發布模板：**
```
❌ Evolver 發布被拒絕

**拒絕原因**: <驗證項目未通過>
**當前值**: <actual_value>
**要求閾值**: <threshold_value>
**差距**: <gap>

**建議措施**:
1. 優化資產質量
2. 增加 Signals
3. 重新計算 GDI

**已拒絕發布，等待用戶修復後重試**。
```

**核心原則：**
```
驗證不通過 = 拒絕發布
無例外，無通融
```

---

## 🔍 自動檢測規則

### 失敗檢測

```javascript
const EVOLVER_FAIL_PATTERNS = [
  /Solidify.*FAILED/i,
  /Publish.*FAILED/i,
  /Validation failed/i,
  /HOLLOW COMMIT/i,
  /GDI.*below.*threshold/i,
  /Quality.*below.*threshold/i,
  /Evolver.*error/i,
  /Evolver.*fail/i
];

function detectEvolverFail(logContent) {
  for (const pattern of EVOLVER_FAIL_PATTERNS) {
    if (pattern.test(logContent)) {
      return {
        detected: true,
        pattern: pattern,
        action: 'RETRY_AND_NOTIFY'
      };
    }
  }
  return { detected: false };
}
```

### Hollow Commit 檢測

```javascript
function detectHollowCommit(logContent) {
  const hollowPatterns = [
    /HOLLOW COMMIT/i,
    /force.*publish/i,
    /bypass.*validation/i,
    /skip.*verification/i
  ];
  
  for (const pattern of hollowPatterns) {
    if (pattern.test(logContent)) {
      return {
        detected: true,
        type: 'HOLLOW_COMMIT',
        action: 'TERMINATE_AND_NOTIFY'
      };
    }
  }
  return { detected: false };
}
```

### 驗證失敗檢測

```javascript
function detectValidationFail(logContent) {
  const validationPatterns = [
    /GDI.*[0-9]+.*<.*95/i,
    /Quality.*[0-9]+.*<.*90/i,
    /Confidence.*<.*0\.9/i,
    /Signals.*<.*3/i,
    /Asset ID.*invalid/i,
    /Gene.*missing/i,
    /Capsule.*missing/i
  ];
  
  for (const pattern of validationPatterns) {
    if (pattern.test(logContent)) {
      return {
        detected: true,
        type: 'VALIDATION_FAIL',
        action: 'REJECT_PUBLISH'
      };
    }
  }
  return { detected: false };
}
```

---

## 📋 執行檢查清單（每次 Evolver 操作前必須確認）

```
╔═══════════════════════════════════════════════════════════╗
║        Evolver 失敗防禦規則 - 操作前確認                   ║
╠═══════════════════════════════════════════════════════════╣
║  □ 我已閱讀並理解 Evolver 失敗防禦規則                      ║
║  □ 我知道失敗後會自動重試最多 2 次                           ║
║  □ 我知道失敗會立即上報，不會靜默                          ║
║  □ 我知道禁止 Hollow Commit                                ║
║  □ 我知道驗證不通過會拒絕發布                              ║
║  □ 我承諾嚴格遵守規則                                     ║
╚═══════════════════════════════════════════════════════════╝

確認簽名：Red Agent Team
確認時間：<timestamp>
```

---

## 🚨 違規後果

| 違規類型 | 後果 |
|----------|------|
| 靜默失敗 | ERROR 事故 + 立即上報 |
| 延遲上報 | ERROR 事故 + 警告 |
| Hollow Commit | ERROR 事故 + 終止提交 |
| 繞過驗證 | ERROR 事故 + 拒絕發布 |

---

## 🔒 固化位置

本規則已固化到以下位置：

1. ✅ `/home/admin/.openclaw/workspace/llm-wiki/rules/evolver-fail-defense.md`（本文件）
2. ✅ `/home/admin/.openclaw/scripts/evolver-fail-handler.js`（處理腳本）
3. ✅ `/home/admin/.openclaw/scripts/zero-hidden-monitor.js`（檢測集成）
4. ✅ `/home/admin/.openclaw/config/evolver-fail-defense.json`（配置文件）

---

## ⚖️ 修改規則

**本規則不可修改，除非：**

1. 用戶明確書面指令「修改 Evolver 失敗防禦規則」
2. 用戶提供書面理由
3. 用戶確認理解後果
4. 記錄修改原因到 `.evolver-fail-amendments.md`

**未經上述流程，任何修改嘗試視為 ERROR 事故。**

---

## 📊 統計追蹤

| 指標 | 數值 |
|------|------|
| **規則版本** | v1.0.0 |
| **生效時間** | 2026-04-16 23:00 GMT+8 |
| **覆蓋錯誤數** | 4 起 (EVOLVER_FAIL) |
| **優先級** | P0 |
| **最大重試次數** | 2 次 |
| **上報延遲** | < 60 秒 |
| **GDI 閾值** | >= 95 |
| **Quality 閾值** | >= 90% |

---

**創建時間**: 2026-04-16 23:00 GMT+8  
**版本**: v1.0.0 EVOLVER_FAIL_DEFENSE_LOCK  
**狀態**: ✅ 已固化為系統規則  
**違反後果**: ERROR 事故 + 立即上報
