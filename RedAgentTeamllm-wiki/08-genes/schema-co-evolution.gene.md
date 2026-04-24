# Gene: Schema Co-Evolution

**gene_id**: `GENE_008_SCHEMA_CO_EVOLUTION`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: RedAgentTeamllm-wiki LLM Wiki Original 2026-04-04  
**category**: 協同進化  
**risk_level**: low  
**creator**: Red AgentTeam  
**created_at**: 2026-04-17T05:45:00Z

---

## 📝 Summary

Schema is co-evolved with LLM; defines structure, workflows for the agent to follow strictly.

Schema 由人類和 LLM 協同進化；定義結構和工作流，Agent 嚴格遵守。

---

## 🎯 Content

**Schema 協同進化定義**:

schema.md 不是靜態文檔，而是由人類和 LLM 共同進化的活文檔。

### 進化流程

#### 1. LLM 發現問題 (LLM Discovers)
LLM 在實踐中發現:
- 現有規範不清晰
- 缺少某項規則
- 規則與實踐衝突
- 需要新的工作流

#### 2. LLM 提議修改 (LLM Proposes)
LLM 向人類提議:
- 修改原因
- 具體修改內容
- 預期影響
- 風險評估

#### 3. 人類審批 (Human Approves)
人類審核提議:
- 理解修改原因
- 評估風險
- 提出反饋
- 批准或拒絕

#### 4. 共同更新 (Both Update)
如批准:
- 更新 schema.md
- 記錄變更原因
- 追加 log.md
- Git commit

#### 5. LLM 遵守 (LLM Follows)
LLM 嚴格遵守新規範:
- 更新內部規則
- 按新規範執行
- 監控合規性

### 進化原則

#### 穩定性優先
- 避免頻繁變更
- 每次變更必須有明確理由
- 變更後需要適應期

#### 雙向反饋
- LLM → 人類：實踐反饋
- 人類 → LLM：戰略指導

#### 記錄完整
- 每次變更必須記錄原因
- log.md 追加變更日志
- Git commit 保留歷史

#### 漸進式進化
- 小步快跑，避免大改
- 先試點，後推廣
- 允許回滾

### 什麼觸發進化?

#### LLM 觸發
- 遇到規範未覆蓋的情況
- 規範阻礙效率
- 發現更好的實踐
- 重複性問題需要規則化

#### 人類觸發
- 戰略方向調整
- 新需求出現
- 外部環境變化
- 審計合規要求

### 與 .learnings/ 的關係

`.learnings/` 中的事故和教訓是 Schema 進化的重要輸入:

- P0 事故 → 可能需要新規則
- 重複違規 → 現有規則執行不力
- 系統性失效 → 需要架構調整

**示例進化路徑**:

```
事故發生 (Clash 禁令違反 30 次)
  ↓
根因分析 (缺少事前檢查機制)
  ↓
LLM 提議 (添加事前檢查規則)
  ↓
人類審批 (批准)
  ↓
更新 schema.md (添加檢查步驟)
  ↓
更新 SOUL.md (強化禁令)
  ↓
LLM 遵守 (執行新規則)
```

---

## 🧬 Signals

`schema`, `co_evolution`, `LLM_proposal`, `human_approval`, `iterative`, `feedback_loop`, `stability`, `documentation`, `git_history`, `accident_driven`

---

## 📋 Strategy

### 步驟 1: 監控實踐問題
LLM 在日常工作中記錄規範相關問題。

### 步驟 2: 定期審查
每周審查問題列表，識別進化機會。

### 步驟 3: 形成提議
將問題轉化為具體的 schema 修改提議。

### 步驟 4: 人類審批
提交人類審核，討論並修改。

### 步驟 5: 執行變更
批准後更新 schema，記錄變更，遵守新規範。

---

## ✅ Validation

```bash
# 1. 檢查 schema.md 是否存在
test -f /home/admin/.openclaw/workspace/llm-wiki/schema.md && echo "✅ schema.md exists"

# 2. 檢查 schema.md 版本歷史
cd /home/admin/.openclaw/workspace && git log --oneline -- llm-wiki/schema.md

# 3. 檢查 log.md 是否有 schema 變更記錄
grep -i "schema\|規範\|變更" /home/admin/.openclaw/workspace/llm-wiki/log.md

# 4. 檢查是否有待審批的提議
find /home/admin/.openclaw/workspace -name "*proposal*.md" -o -name "*schema-change*.md" 2>/dev/null

# 5. 檢查 .learnings/ 是否驅動過 schema 變更
grep -r "schema\|CONSTITUTION" /home/admin/.openclaw/workspace/.learnings/*.md | head -10
```

---

## 🔒 Constraints

- **必須**: Schema 變更必須人類審批
- **必須**: 變更必須記錄原因
- **必須**: 變更必須追加 log.md
- **必須**: LLM 必須遵守最新 schema
- **禁止**: LLM 單方面修改 schema
- **禁止**: 頻繁變更 (穩定性優先)
- **必須**: 變更後 Git commit

---

## 📊 Metrics

| 指標 | 目標值 | 當前值 |
|------|--------|--------|
| Schema 變更次數 | <1 次/月 | 待測量 |
| LLM 提議數 | 2-4 次/月 | 待測量 |
| 人類批准率 | >70% | 待測量 |
| 變更記錄完整率 | 100% | 待測量 |
| 合規率 | 100% | 待測量 |

---

## 🔗 References

- RedAgentTeamllm-wiki LLM Wiki Original 2026-04-04
- `/home/admin/.openclaw/workspace/llm-wiki/schema.md`
- `/home/admin/.openclaw/workspace/.learnings/CONSTITUTION.md`
- `/home/admin/.openclaw/workspace/SOUL.md`

---

**狀態**: ✅ Active  
**最後驗證**: 2026-04-17 05:45 GMT+8
