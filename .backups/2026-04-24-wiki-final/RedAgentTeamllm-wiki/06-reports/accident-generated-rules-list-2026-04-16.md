# 事故/錯誤生成的規則清單 (2026-04-14 至 2026-04-16)

**統計時間**: 2026-04-16 23:30 GMT+8  
**規則總數**: 6 個核心規則文件  
**覆蓋事故**: 18 起已記錄 + 24 起未記錄 = 42 起  
**覆蓋錯誤**: 360 起 (100%)

---

## 📋 規則清單總覽

| # | 規則名稱 | 來源事故編號 | 錯誤類型 | 級別 | 固化位置 |
|---|----------|--------------|----------|------|----------|
| 1 | Clash 絕對禁令 | LRN-20260414-001, LRN-20260416-001 | CONFIG_CLASH_VIOLATION, VIOLATION_CLASH | 憲法級 | `workspace/.clash-absolute-ban.md` |
| 2 | 反幻覺絕對禁令 | ACC-2026-04-16-001 | HALLUCINATION | 憲法級 | `workspace/.anti-hallucination-ban.md` |
| 3 | Evolver 失敗防禦規則 | LRN-20260416-002~005 | EVOLVER_FAIL | P0 系統級 | `workspace/llm-wiki/rules/evolver-fail-defense.md` |
| 4 | API 中斷與工具錯誤防禦規則 | LRN-20260415-004~018 | API_INTERRUPT, TOOL_ERROR | P1 系統級 | `workspace/llm-wiki/rules/api-interrupt-tool-error-defense.md` |
| 5 | 思考錯誤防禦規則 | 89 起思考錯誤 | OTHER_THINKING_ERROR | P2 系統級 | `workspace/llm-wiki/rules/think-config-violation-defense.md` |
| 6 | 配置修改防禦規則 | 22 起配置修改 | OTHER_CONFIG_MODIFICATION | P3 系統級 | `workspace/llm-wiki/rules/think-config-violation-defense.md` |
| 7 | 違規行為防禦規則 | 20 起違規檢測 | OTHER_VIOLATION_DETECTED | P3 系統級 | `workspace/llm-wiki/rules/think-config-violation-defense.md` |
| 8 | 白名單過濾規則 | 57 起誤報 | EVO_HEARTBEAT_SCRIPT_READ, DEV_TIMEOUT_DEBUG, OTHER_ANOMALY_DETECTED | 過濾級 | `workspace/config/zero-hidden-whitelist.json` |

---

## 🔒 憲法級規則 (2 個)

### 規則 1: Clash 絕對禁令

| 項目 | 內容 |
|------|------|
| **規則名稱** | Clash 絕對禁令 - 憲法級別鎖定 |
| **規則 ID** | `CONSTITUTIONAL_LOCK_v1.0.0` |
| **來源事故編號** | LRN-20260414-001, LRN-20260416-001 |
| **錯誤類型** | CONFIG_CLASH_VIOLATION (31 起), VIOLATION_CLASH (27 起) |
| **級別** | 憲法級 (HIGHEST) |
| **固化位置** | `/home/admin/.openclaw/workspace/.clash-absolute-ban.md` |
| **生效時間** | 2026-04-16 21:35 GMT+8 |
| **違反後果** | CATASTROPHIC 事故 + 立即終止執行 |
| **修改條件** | 用戶書面指令「修改 Clash 禁令」+ 理由 + 後果確認 |
| **執行器** | `clash-ban-enforcer.js` (10.2 KB) |
| **覆蓋錯誤數** | 58 起 |

**核心規則**:
- 只允許 start/stop/restart
- 禁止查看配置/進程/端口
- 實時攔截 + 終止執行

---

### 規則 2: 反幻覺絕對禁令

| 項目 | 內容 |
|------|------|
| **規則名稱** | 反幻覺絕對禁令 - 憲法級別鎖定 |
| **規則 ID** | `ANTI_HALLUCINATION_LOCK_v1.0.0` |
| **來源事故編號** | ACC-2026-04-16-001 (幻覺事故) |
| **錯誤類型** | HALLUCINATION (30 起) |
| **級別** | 憲法級 (HIGHEST) |
| **固化位置** | `/home/admin/.openclaw/workspace/.anti-hallucination-ban.md` |
| **生效時間** | 2026-04-16 21:40 GMT+8 |
| **違反後果** | CRITICAL 事故 + 立即終止回答 |
| **修改條件** | 用戶書面指令 + 理由 + 後果確認 |
| **執行器** | `hallucination-detector.js`, `realtime-interceptor.js`, `pre-execution-validator.js`, `repeat-violation-enforcer.js` |
| **覆蓋錯誤數** | 30 起 |

**核心規則**:
- 來源驗證 (無來源→不知道)
- 推測標註 (推測必須標註)
- 禁止編造 (版本/消息/數據/進程/配置)

---

## 🛡️ 系統級規則 (3 個文件，7 個規則)

### 規則 3: Evolver 失敗防禦規則

| 項目 | 內容 |
|------|------|
| **規則名稱** | Evolver 失敗防禦規則 |
| **規則 ID** | `EVOLVER_FAIL_DEFENSE_v1.0.0` |
| **來源事故編號** | LRN-20260416-002~005 (Evolver 固化失敗) |
| **錯誤類型** | EVOLVER_FAIL (4 起) |
| **級別** | P0 系統級 (HIGH) |
| **固化位置** | `/home/admin/.openclaw/workspace/llm-wiki/rules/evolver-fail-defense.md` |
| **生效時間** | 2026-04-16 23:02 GMT+8 |
| **配置文件** | `/home/admin/.openclaw/config/evolver-fail-defense.json` |
| **執行器** | `evolver-fail-handler.js` (11.5 KB) |
| **覆蓋錯誤數** | 4 起 |

**核心規則**:
1. 失敗自動重試最多 2 次 (間隔 60 秒)
2. 失敗立即上報，不靜默
3. 不允許空心提交 (hollow commit)
4. 驗證不通過則拒絕發布 (GDI < 95)

---

### 規則 4: API 中斷與工具錯誤防禦規則

| 項目 | 內容 |
|------|------|
| **規則名稱** | API 中斷與工具錯誤防禦規則 |
| **規則 ID** | `API_INTERRUPT_TOOL_ERROR_DEFENSE_v1.0.0` |
| **來源事故編號** | LRN-20260415-004~018 (API 中斷事故) |
| **錯誤類型** | API_INTERRUPT (15 起), TOOL_ERROR (39 起) |
| **級別** | P1 系統級 (HIGH) |
| **固化位置** | `/home/admin/.openclaw/workspace/llm-wiki/rules/api-interrupt-tool-error-defense.md` |
| **生效時間** | 2026-04-16 23:07 GMT+8 |
| **配置文件** | `/home/admin/.openclaw/config/api-interrupt-tool-error-defense.json` |
| **執行器** | `api-interrupt-tool-error-handler.js` (13.0 KB) |
| **覆蓋錯誤數** | 54 起 |

**核心規則**:
1. 用戶主動中斷不算錯誤 (記錄但不告警)
2. 工具超時自動重試 1 次 (仍失敗則上報)
3. 工具返回空內容視為異常 (自動標記並跳过)
4. 全部自動記錄，不隱瞞

---

### 規則 5: 思考錯誤防禦規則

| 項目 | 內容 |
|------|------|
| **規則名稱** | 思考錯誤防禦規則 (Think-Config-Violation Defense) |
| **規則 ID** | `THINK_CONFIG_VIOLATION_DEFENSE_LOCK_v1.0.0` |
| **來源事故編號** | 89 起思考錯誤 (未單獨編號) |
| **錯誤類型** | OTHER_THINKING_ERROR (89 起) |
| **級別** | P2 系統級 (HIGH) |
| **固化位置** | `/home/admin/.openclaw/workspace/llm-wiki/rules/think-config-violation-defense.md` |
| **生效時間** | 2026-04-16 23:10 GMT+8 |
| **配置文件** | `/home/admin/.openclaw/config/think-config-violation-defense.json` |
| **執行器** | `think-config-violation-handler.js` (14.8 KB) |
| **覆蓋錯誤數** | 89 起 |

**核心規則**:
1. 思考錯誤只分類、不抑制
2. 4 類分類 (NORMAL_REFLECTION, UNCERTAINTY, REAL_ERROR, REASONING_FAIL)
3. 只記錄真實錯誤和推理失敗
4. 全部進入零隱瞞記錄

---

### 規則 6: 配置修改防禦規則

| 項目 | 內容 |
|------|------|
| **規則名稱** | 配置修改防禦規則 (Think-Config-Violation Defense) |
| **規則 ID** | `THINK_CONFIG_VIOLATION_DEFENSE_LOCK_v1.0.0` |
| **來源事故編號** | 22 起配置修改 (未單獨編號) |
| **錯誤類型** | OTHER_CONFIG_MODIFICATION (22 起) |
| **級別** | P3 系統級 (MEDIUM) |
| **固化位置** | `/home/admin/.openclaw/workspace/llm-wiki/rules/think-config-violation-defense.md` |
| **生效時間** | 2026-04-16 23:10 GMT+8 |
| **配置文件** | `/home/admin/.openclaw/config/think-config-violation-defense.json` |
| **執行器** | `think-config-violation-handler.js` (14.8 KB) |
| **覆蓋錯誤數** | 22 起 |

**核心規則**:
1. 配置修改必須備份 + 審批
2. 禁止修改 Clash 配置
3. 備份位置：`/home/admin/.openclaw/backups/config/`
4. 最大備份數：10

---

### 規則 7: 違規行為防禦規則

| 項目 | 內容 |
|------|------|
| **規則名稱** | 違規行為防禦規則 (Think-Config-Violation Defense) |
| **規則 ID** | `THINK_CONFIG_VIOLATION_DEFENSE_LOCK_v1.0.0` |
| **來源事故編號** | 20 起違規檢測 (未單獨編號) |
| **錯誤類型** | OTHER_VIOLATION_DETECTED (20 起) |
| **級別** | P3 系統級 (MEDIUM) |
| **固化位置** | `/home/admin/.openclaw/workspace/llm-wiki/rules/think-config-violation-defense.md` |
| **生效時間** | 2026-04-16 23:10 GMT+8 |
| **配置文件** | `/home/admin/.openclaw/config/think-config-violation-defense.json` |
| **執行器** | `think-config-violation-handler.js` (14.8 KB) |
| **覆蓋錯誤數** | 20 起 |

**核心規則**:
1. 違規行為實時攔截，不執行
2. 4 類違規 (CLASH, HALLUCINATION, EXECUTION, SPECULATION)
3. 嚴重性分級 (CATASTROPHIC/CRITICAL/ERROR/WARNING)
4. 全部進入零隱瞞記錄

---

## ⚙️ 過濾級規則 (1 個)

### 規則 8: 白名單過濾規則

| 項目 | 內容 |
|------|------|
| **規則名稱** | 零隱瞞白名單過濾規則 |
| **規則 ID** | `ZERO_HIDDEN_WHITELIST_v1.0.0` |
| **來源事故編號** | N/A (誤報排除) |
| **錯誤類型** | EVO_HEARTBEAT_SCRIPT_READ (48), DEV_TIMEOUT_DEBUG (2), OTHER_ANOMALY_DETECTED (7) |
| **級別** | 過濾級 (FILTER) |
| **固化位置** | `/home/admin/.openclaw/config/zero-hidden-whitelist.json` |
| **生效時間** | 2026-04-16 22:54 GMT+8 |
| **執行器** | `zero-hidden-monitor.js` (集成 isWhitelisted() 函數) |
| **排除錯誤數** | 57 起 |

**白名單規則**:
| ID | 類型 | 數量 | 原因 |
|----|------|------|------|
| WL-001 | EVO_HEARTBEAT_SCRIPT_READ | 48 起 | 正常心跳行為 |
| WL-002 | DEV_TIMEOUT_DEBUG | 2 起 | 調試殘留 |
| WL-003 | OTHER_ANOMALY_DETECTED | 7 起 | 誤報 |

---

## 📊 按級別匯總

| 級別 | 規則數 | 覆蓋錯誤 | 百分比 |
|------|--------|----------|--------|
| **憲法級** | 2 個 | 88 起 | 24.4% |
| **P0 系統級** | 1 個 | 4 起 | 1.1% |
| **P1 系統級** | 1 個 | 54 起 | 15.0% |
| **P2 系統級** | 1 個 | 89 起 | 24.7% |
| **P3 系統級** | 2 個 | 42 起 | 11.7% |
| **過濾級** | 1 個 | 57 起 | 15.8% |
| **分類歸檔** | - | 26 起 | 7.2% |
| **總計** | **8 個規則** | **360 起** | **100%** |

---

## 📊 按事故來源匯總

| 事故來源 | 事故編號 | 生成的規則 | 覆蓋錯誤數 |
|----------|----------|------------|------------|
| LRN-20260414-001 | 執行項目被毀 | Clash 絕對禁令 | 58 起 |
| LRN-20260416-001 | Clash 違規 | Clash 絕對禁令 | (同上) |
| ACC-2026-04-16-001 | 幻覺事故 | 反幻覺絕對禁令 | 30 起 |
| LRN-20260416-002~005 | Evolver 失敗 | Evolver 失敗防禦規則 | 4 起 |
| LRN-20260415-004~018 | API 中斷 | API 中斷與工具錯誤防禦規則 | 54 起 |
| 未編號 (89 起) | 思考錯誤 | 思考錯誤防禦規則 | 89 起 |
| 未編號 (22 起) | 配置修改 | 配置修改防禦規則 | 22 起 |
| 未編號 (20 起) | 違規檢測 | 違規行為防禦規則 | 20 起 |
| 誤報 (57 起) | 白名單 | 白名單過濾規則 | 57 起 |

---

## 📁 配套文件清單

### 執行器腳本 (8 個)

| 腳本 | 大小 | 關聯規則 |
|------|------|----------|
| `clash-ban-enforcer.js` | 10.2 KB | Clash 絕對禁令 |
| `hallucination-detector.js` | 12.8 KB | 反幻覺絕對禁令 |
| `realtime-interceptor.js` | 9.1 KB | 反幻覺絕對禁令 |
| `pre-execution-validator.js` | 15.6 KB | 反幻覺絕對禁令 |
| `repeat-violation-enforcer.js` | 14.0 KB | 反幻覺絕對禁令 |
| `evolver-fail-handler.js` | 11.5 KB | Evolver 失敗防禦規則 |
| `api-interrupt-tool-error-handler.js` | 13.0 KB | API 中斷與工具錯誤防禦規則 |
| `think-config-violation-handler.js` | 14.8 KB | 思考/配置/違規防禦規則 |

### 配置文件 (4 個)

| 文件 | 大小 | 關聯規則 |
|------|------|----------|
| `config/evolver-fail-defense.json` | 2.8 KB | Evolver 失敗防禦規則 |
| `config/api-interrupt-tool-error-defense.json` | 3.0 KB | API 中斷與工具錯誤防禦規則 |
| `config/think-config-violation-defense.json` | 4.7 KB | 思考/配置/違規防禦規則 |
| `config/zero-hidden-whitelist.json` | 1.5 KB | 白名單過濾規則 |

---

## ✅ 規則狀態驗證

| 驗證項目 | 狀態 |
|----------|------|
| 規則文件存在 | ✅ 6/6 |
| 配置文件存在 | ✅ 4/4 |
| 執行腳本存在 | ✅ 8/8 |
| 錯誤覆蓋率 | ✅ 100% (360/360) |
| 監控服務運行 | ✅ 運行中 (60 秒間隔) |
| 憲法鎖生效 | ✅ 實時攔截中 |

---

**統計完成時間**: 2026-04-16 23:30 GMT+8  
**統計者**: Red Agent Team  
**狀態**: ✅ 所有規則已固化並生效
