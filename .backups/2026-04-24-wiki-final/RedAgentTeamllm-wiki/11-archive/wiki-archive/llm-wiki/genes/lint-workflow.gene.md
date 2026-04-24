---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Lint Workflow.Gene
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
# Gene: Lint Workflow

**gene_id**: `GENE_005_LINT_WORKFLOW`  
**type**: Gene  
**version**: 1.0.0  
**schema_version**: 1.5.0  
**source**: Karpathy LLM Wiki Original 2026-04-04  
**category**: 工作流  
**risk_level**: low  
**creator**: Red AgentTeam  
**created_at**: 2026-04-17T05:45:00Z

---

## 📝 Summary

Lint: detect contradictions, stale claims, orphan pages, missing cross-references, gaps; auto-repair where possible.

健康檢查：檢測矛盾、過時聲明、孤兒頁面、缺失交叉引用、知識缺口；盡可能自動修復。

---

## 🎯 Content

**Lint 工作流定義**:

定期對知識庫進行健康檢查，確保知識質量。

### 檢測項目

#### 1. 矛盾檢測 (Contradictions)
- 檢測不同條目之間的矛盾聲明
- 示例：條目 A 說 X 是 true，條目 B 說 X 是 false
- 修復：標記矛盾，提示人類裁決

#### 2. 過時聲明 (Stale Claims)
- 檢測可能過時的信息
- 示例：「最新版本是 v1.0」但實際已發布 v2.0
- 修復：標記為「可能過時」，建議更新

#### 3. 孤兒頁面 (Orphan Pages)
- 檢測無交叉引用的頁面
- 定義：沒有任何其他頁面引用它
- 修復：添加相關引用或考慮刪除

#### 4. 缺失交叉引用 (Missing Cross-References)
- 檢測應有引用但缺失的頁面
- 示例：提到某概念但無鏈接
- 修復：自動添加交叉引用

#### 5. 知識缺口 (Gaps)
- 檢測知識庫中的空白
- 示例：有 Docker 優化但無 K8s 優化
- 修復：建議人類提供 raw 資料或 LLM 研究補充

### 執行頻率

- **完整 Lint**: 每周一次
- **快速 Lint**: 每次重大更新後
- **緊急 Lint**: 人類手動觸發

### 輸出

- `lint-report-YYYYMMDD.md` - 詳細報告
- log.md 追加記錄
- 自動修復 (如可能)
- 待人類裁決列表

**為什麼重要**:

- 知識庫會隨時間腐爛
- 矛盾降低信任度
- 孤兒頁面浪費存儲
- 缺失引用降低可導航性
- 定期 Lint 保持知識健康

---

## 🧬 Signals

`lint`, `workflow`, `health_check`, `contradictions`, `stale_claims`, `orphan_pages`, `cross_references`, `knowledge_gaps`, `auto_repair`, `weekly`

---

## 📋 Strategy

### 步驟 1: 掃描所有 Wiki 條目
讀取 wiki/ 中的所有 Markdown 文件。

### 步驟 2: 構建引用圖
分析每個文件的引用關係，建立圖結構。

### 步驟 3: 檢測問題
識別孤兒頁面、缺失引用、矛盾等。

### 步驟 4: 自動修復
對可自動修復的問題執行修復。

### 步驟 5: 生成報告
創建 lint-report-YYYYMMDD.md，記錄所有發現。

---

## ✅ Validation

```bash
# 1. 檢查是否有 Lint 報告
ls -la /home/admin/.openclaw/workspace/llm-wiki/wiki/lint-report-*.md

# 2. 檢查最新報告內容
cat /home/admin/.openclaw/workspace/llm-wiki/wiki/lint-report-*.md | tail -50

# 3. 檢查孤兒頁面 (無引用的頁面)
# (需要腳本分析，此為示意)

# 4. 檢查 log.md 是否有 Lint 記錄
grep -i "lint\|健康檢查" /home/admin/.openclaw/workspace/llm-wiki/log.md | tail -5

# 5. 檢查是否有待人類裁決的問題
grep -i "待確認\|需人類\|human_review" /home/admin/.openclaw/workspace/llm-wiki/wiki/lint-report-*.md
```

---

## 🔒 Constraints

- **必須**: 每周至少執行一次完整 Lint
- **必須**: 生成 lint-report-YYYYMMDD.md
- **必須**: 追加 log.md
- **必須**: 自動修復所有可修復問題
- **必須**: 無法修復的問題必須報告人類
- **禁止**: 靜默忽略矛盾
- **禁止**: 刪除孤兒頁面 without 人類確認

---

## 📊 Metrics

| 指標 | 目標值 | 當前值 |
|------|--------|--------|
| Lint 執行頻率 | 1 次/周 | 待測量 |
| 矛盾檢測數 | 0 | 待測量 |
| 孤兒頁面比例 | <5% | 待測量 |
| 自動修復率 | >80% | 待測量 |
| 人類裁決待處理 | <5 | 待測量 |

---

## 🔗 References

- Karpathy LLM Wiki Original 2026-04-04
- `GENE_001_KARPATHY_CORE_IDEAL`
- `/home/admin/.openclaw/workspace/llm-wiki/schema.md`
- `/home/admin/.openclaw/workspace/.learnings/` (事故學習)

---

**狀態**: ✅ Active  
**最後驗證**: 2026-04-17 05:45 GMT+8


## 相關文檔

- [[lint-report-20260417]]
- [[lint-report-20260413]]
- [[lint-report-20260417]]
