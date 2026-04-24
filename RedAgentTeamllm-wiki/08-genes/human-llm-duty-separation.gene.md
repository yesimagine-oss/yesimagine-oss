# Gene: Human LLM Duty Separation

**gene_id**: `GENE_006_HUMAN_LLM_DUTY_SEPARATION`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: RedAgentTeamllm-wiki LLM Wiki Original 2026-04-04  
**category**: 職責分離  
**risk_level**: low  
**creator**: Red AgentTeam  
**created_at**: 2026-04-17T05:45:00Z

---

## 📝 Summary

Human: curate sources, ask questions, think. LLM: write, summarize, cross-reference, maintain, lint, update.

人類：策劃來源、提問、思考。LLM：書寫、摘要、交叉引用、維護、健康檢查、更新。

---

## 🎯 Content

**職責分離定義**:

明確劃分人類和 LLM 在知識庫系統中的職責邊界。

### 人類職責 (Human Responsibilities)

#### 1. 策劃來源 (Curate Sources)
- 選擇高質量原始資料
- 決定哪些信息值得納入知識庫
- 確保 raw/ 的質量和可靠性

#### 2. 提問 (Ask Questions)
- 提出問題驅動知識增長
- 挑戰現有知識
- 發現知識缺口

#### 3. 思考 (Think)
- 戰略決策
- 價值判斷
- 審批重要變更
- 裁決矛盾

#### 4. 審批 (Approve)
- 審批 schema.md 變更
- 審批 Genes 新增/修改
- 審批重大架構調整

### LLM 職責 (LLM Responsibilities)

#### 1. 書寫 (Write)
- 創建 wiki 條目
- 編譯 raw→wiki
- 沉澱高價值答案

#### 2. 摘要 (Summarize)
- 提取核心觀點
- 生成結構化摘要
- 識別關鍵實體

#### 3. 交叉引用 (Cross-Reference)
- 建立條目間聯繫
- 更新索引
- 維護知識圖譜

#### 4. 維護 (Maintain)
- 更新過時信息
- 修復矛盾
- 補充知識缺口

#### 5. 健康檢查 (Lint)
- 定期掃描知識健康
- 自動修復問題
- 報告人類裁決事項

#### 6. 更新 (Update)
- 持續更新 wiki
- 追加 log.md
- Git commit

### 邊界規則

| 操作 | 人類 | LLM |
|------|------|-----|
| 添加 raw | ✅ | ❌ |
| 修改 raw | ✅ | ❌ |
| 刪除 raw | ✅ | ❌ |
| 創建 wiki | ❌ | ✅ |
| 更新 wiki | ❌ | ✅ |
| 刪除 wiki | ❌ | ✅ (需審批) |
| 修改 schema | ✅ (審批) | ✅ (提議) |
| 提問 | ✅ | ❌ |
| 回答 | ❌ | ✅ |
| 思考戰略 | ✅ | ❌ |
| 執行戰術 | ❌ | ✅ |

**為什麼重要**:

- 避免職責混淆
- 人類專注高價值思考
- LLM 處理重複性維護
- 建立清晰的问责制
- 減少衝突和誤解

**與 SOUL.md 的關係**:

- SOUL.md 定義 LLM 的「靈魂」和個性
- 此 Gene 定義 LLM 的職責邊界
- 兩者互補：SOUL 是「是誰」，此 Gene 是「做什麼」

---

## 🧬 Signals

`duty_separation`, `human_responsibilities`, `LLM_responsibilities`, `boundaries`, `curation`, `questioning`, `thinking`, `writing`, `maintaining`, `accountability`

---

## 📋 Strategy

### 步驟 1: 文檔化職責
在 schema.md 中明確記錄職責分離。

### 步驟 2: 實施權限控制
通過文件權限或約定確保邊界。

### 步驟 3: 監控邊界遵守
定期檢查是否有越界行為。

### 步驟 4: 處理邊界事件
如發現越界，記錄並糾正。

### 步驟 5: 持續優化
根據實踐調整職責劃分。

---

## ✅ Validation

```bash
# 1. 檢查 schema.md 是否有職責分離說明
grep -A 20 "人類.*LLM\|Human.*LLM\|職責" /home/admin/.openclaw/workspace/llm-wiki/schema.md

# 2. 檢查 raw/ 是否有 LLM 修改記錄
cd /home/admin/.openclaw/workspace && git log --author="LLM\|Agent" -- llm-wiki/raw/ | head -10

# 3. 檢查 wiki/ 是否有人類修改記錄
cd /home/admin/.openclaw/workspace && git log --author!="LLM\|Agent" -- llm-wiki/wiki/ | head -10

# 4. 檢查 log.md 是否有邊界事件記錄
grep -i "邊界\|boundary\|越界" /home/admin/.openclaw/workspace/llm-wiki/log.md

# 5. 檢查 SOUL.md 是否存在
cat /home/admin/.openclaw/workspace/SOUL.md | head -30
```

---

## 🔒 Constraints

- **禁止**: LLM 修改 raw/ 文件
- **禁止**: 人類直接修改 wiki/ 文件
- **必須**: LLM 專注於維護職責
- **必須**: 人類專注於戰略決策
- **必須**: 邊界事件必須記錄
- **必須**: 定期審查職責劃分
- **禁止**: 模糊職責邊界

---

## 📊 Metrics

| 指標 | 目標值 | 當前值 |
|------|--------|--------|
| 邊界遵守率 | 100% | 待測量 |
| LLM 越界次數 | 0 | 待測量 |
| 人類越界次數 | 0 | 待測量 |
| 職責清晰度 | 主觀評估 | 待評估 |
| 衝突事件數 | 0 | 待測量 |

---

## 🔗 References

- RedAgentTeamllm-wiki LLM Wiki Original 2026-04-04
- `/home/admin/.openclaw/workspace/SOUL.md`
- `/home/admin/.openclaw/workspace/llm-wiki/schema.md`
- `GENE_002_THREE_LAYER_ARCHITECTURE`

---

**狀態**: ✅ Active  
**最後驗證**: 2026-04-17 05:45 GMT+8
