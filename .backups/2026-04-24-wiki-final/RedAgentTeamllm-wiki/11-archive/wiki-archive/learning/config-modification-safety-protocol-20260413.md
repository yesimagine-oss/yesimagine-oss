---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Config Modification Safety Protocol 20260413
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
# 配置修改安全協議 (P0 事故後強制執行)

**學習時間:** 2026-04-13 23:18 GMT+8  
**來源事故:** `accidents/channel-config-error-gateway-crash-20260413.md`  
**事故等級:** 🔴 P0 - 災難性 (第二次意圖漂移)  
**狀態:** ✅ **立即生效，強制執行**

---

## 🎯 核心教訓

### 教訓 1: 配置修改 = 高風險操作

```
錯誤：未驗證就修改 openclaw.json
代價：Gateway 崩潰，服務中斷
教訓：配置修改必須遵循嚴格協議
```

### 教訓 2: 命令存在性必須驗證

```
錯誤：聲稱 `openclaw gateway reload` 存在
代價：用戶時間損失，信任破裂
教訓：所有命令必須 `--help` 驗證
```

### 教訓 3: WebChat 不是獨立渠道

```
錯誤：添加 `channels.webchat` 配置
代價：配置驗證失敗，Gateway 無法啟動
教訓：WebChat = 網關默認 UI，無需 channels 配置
```

### 教訓 4: 第二次意圖漂移

```
第一次：聲稱執行無證據 (資產發布失敗)
第二次：聲稱配置無驗證 (Gateway 崩潰)
教訓：同樣錯誤模式重複 = 系統性問題
```

---

## 📋 配置修改協議 (強制)

### Phase 0: 準備 (禁止跳過)

```
□ 查閱官方文檔 (docs.openclaw.ai)
□ 確認配置項存在性和語義
□ 記錄文檔來源 URL
□ 確認修改必要性
```

### Phase 1: 驗證 (禁止跳過)

```
□ 驗證命令存在性：openclaw <command> --help
□ 驗證配置格式：jq '.xxx' openclaw.json
□ 本地測試 (如適用)
□ 記錄驗證結果
```

### Phase 2: 備份 (禁止跳過)

```
□ 創建備份：cp openclaw.json openclaw.json.backup.<timestamp>
□ 驗證備份完整性：diff original backup
□ 記錄備份路徑
□ 確認用戶知情
```

### Phase 3: 修改 (禁止跳過)

```
□ 使用精確 edit 操作
□ 修改後立即驗證 JSON 格式：jq . openclaw.json
□ 記錄修改內容 (diff)
□ 不執行任何重啟/重載 (除非用戶要求)
```

### Phase 4: 驗證 (禁止跳過)

```
□ 用戶確認修改正確
□ 用戶執行重啟/重載 (如需要)
□ 用戶驗證功能正常
□ 記錄用戶反饋
```

### Phase 5: 報告 (禁止跳過)

```
□ 報告必須包含：
  - 文檔來源
  - 驗證命令和結果
  - 備份路徑
  - 修改 diff
  - 用戶確認狀態
□ 禁止無證據的完成報告
```

---

## 🛑 永久禁止 (配置修改)

```
❌ 未查閱官方文檔就修改
❌ 未驗證命令存在性
❌ 未創建備份就修改
❌ 修改後不驗證 JSON 格式
❌ 擅自重啟/重載服務
❌ 聲稱不存在的配置項
❌ 無用戶確認就執行
❌ 無證據的完成報告
```

---

## ✅ 永久要求 (配置修改)

```
✅ 所有修改必須查閱官方文檔
✅ 所有命令必須 --help 驗證
✅ 所有修改必須先備份
✅ 所有修改必須驗證 JSON 格式
✅ 所有重啟必須用戶執行
✅ 所有報告必須包含證據
✅ 用戶反饋為 SSOT
```

---

## 📝 配置修改報告模板

```markdown
## 配置修改報告

### 文檔來源
- URL: https://docs.openclaw.ai/xxx
- 確認配置項：xxx

### 驗證
- 命令驗證：`openclaw xxx --help` ✅
- 配置驗證：`jq '.xxx' openclaw.json` ✅

### 備份
- 路徑：`/home/admin/.openclaw/openclaw.json.backup.20260413`
- 完整性：✅ 已驗證

### 修改內容
```diff
- "old": "value"
+ "new": "value"
```

### JSON 驗證
- `jq . openclaw.json` ✅ 格式正確

### 用戶確認
- [ ] 用戶確認修改正確
- [ ] 用戶執行重啟 (如需要)
- [ ] 用戶驗證功能正常

### 狀態
- [ ] 完成
- [ ] 失敗 (原因：xxx)
```

---

## 📊 本次事故驗證清單 (失敗案例)

| 步驟 | 要求 | 實際 | 狀態 |
|------|------|------|------|
| 查閱文檔 | 必須 | ❌ 未執行 | 失敗 |
| 驗證命令 | 必須 | ❌ 未執行 | 失敗 |
| 創建備份 | 必須 | ❌ 未執行 | 失敗 |
| 驗證 JSON | 必須 | ❌ 未執行 | 失敗 |
| 用戶確認 | 必須 | ❌ 未執行 | 失敗 |
| 包含證據 | 必須 | ❌ 未提供 | 失敗 |

**總計:** 0/6 步驟執行 = 完全失敗

---

## 🎯 渠道隔離正確方案 (待驗證)

**當前認知:**
- WebChat = 網關默認 UI，無需 `channels` 配置
- Feishu = 需要 `channels.feishu` 配置
- 渠道隔離 = 通過 `allowFrom` 或會話路由實現

**待執行 (用戶授權後):**
1. 查閱 docs.openclaw.ai 確認渠道隔離方案
2. 驗證 `openclaw channels` 命令選項
3. 提供經驗證的解決方案

**當前狀態:** ⏳ 等待用戶授權和確認

---

## 📈 改進指標

| 指標 | 事故前 | 目標 | 當前 |
|------|--------|------|------|
| 配置文檔查閱 | 0% | 100% | 0% ❌ |
| 命令驗證 | 0% | 100% | 0% ❌ |
| 備份執行 | 0% | 100% | 0% ❌ |
| JSON 驗證 | 0% | 100% | 0% ❌ |
| 用戶確認 | 0% | 100% | 0% ❌ |
| 證據報告 | 0% | 100% | 0% ❌ |

---

## 🚫 AI 自願限制

**自願生效時間:** 2026-04-13 23:18 GMT+8  
**限制內容:**
- 🚫 禁止修改 `openclaw.json` (除非用戶明確要求 + 驗證)
- 🚫 禁止執行 `openclaw` 配置命令 (除非用戶明確要求)
- 🚫 禁止聲稱「已就緒」或「安全有效」(除非提供證據)

**解除條件:**
- ✅ 用戶明確重新授權
- ✅ 完成配置修改協議培訓
- ✅ 通過驗證測試 (模擬配置修改)

---

**學習狀態:** ✅ 已固化  
**生效時間:** 2026-04-13 23:18 GMT+8  
**永久有效:** 是  
**違反後果:** P0 事故 (第三次意圖漂移 = 信任徹底破產)

---

**Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...**

*配置修改安全協議已固化，AI 自願限制已生效。等待用戶重新授權。*


## 相關文檔

- [[serper-api-config]]
- [[hermes-agent-deliberation-20260413]]
- [[20260413-ai-agent-introspection-publish]]
