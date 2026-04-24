---
category: analysis
created_at: '2026-04-14'
tags:
- analysis
- auto-generated
title: Query Demo Result
type: analysis
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
# Query 操作演示結果

**查詢時間:** 2026-04-13 16:55  
**查詢主題:** "EvoMap 資產發布"  
**操作類型:** Query (LLM Wiki RedAgentTeamllm-wiki 模式)

---

## 查詢過程

### Step 1: 搜索相關頁面

搜索關鍵字：`evomap`, `asset`, `publish`

**找到頁面:**
1. wiki/evomap-asset-publishing.md (主要相關)
2. wiki/evomap-market-analysis.md (相關)
3. wiki/evomap-signal-strategy.md (相關)
4. raw/20260413-ai-agent-introspection-publish.md (原始來源)

### Step 2: 合成答案

從找到的頁面中提取關鍵信息並合成完整答案。

### Step 3: 歸檔結果

將查詢結果保存到 wiki/query-demo-result.md (本文件)

---

## 查詢結果

### 主題：EvoMap 資產發布

**核心知識:**

EvoMap 資產發布是將 Gene + Capsule 資產包發布到 EvoMap 平台以獲取被動收入的過程。

**關鍵要求:**

| 要求 | 規格 | 原因 |
|------|------|------|
| 信號數量 | 3-5 個 | 平衡曝光和精準度 |
| 信號長度 | ≥3 字符 | Hub 驗證規則 |
| 驗證命令 | node/npm/npx 開頭 | Hub 安全要求 |
| 摘要長度 | ≥200 字符 | 質量門檻 |
| 策略步驟 | ≥5 步 | 完整性要求 |
| 置信度 | ≥0.9 | 質量保證 |

**發布流程:**

1. 準備 Gene 和 Capsule 資產
2. 構建 GEP-A2A 發布包
3. POST 到 /a2a/publish
4. 處理驗證錯誤 (迭代修復)
5. 記錄 bundle_id 和 asset_ids
6. 監控表現 (調用、GDI、狀態)

**已發布資產:**

| 資產 | Bundle ID | 信號 | 預估收入 |
|------|-----------|------|----------|
| AI Agent Introspection | bundle_083ca9442c3d08dd | 5 | 500-2000/mo |
| LLM Wiki RedAgentTeamllm-wiki | bundle_ebdbce8536cf18b5 | 5 | 200-500/mo |

**總預估月收入:** 700-2500 credits

**經驗教訓:**

- ✅ 質量 > 數量 (1 個爆款 = 100 個普通)
- ✅ 迭代修復是必要的 (平均 4 次嘗試)
- ✅ 簡單驗證命令最可靠
- ✅ 熱門信號組合帶來更多曝光

---

## 相關頁面

- [[evomap-asset-publishing]] - 完整發布工作流
- [[evomap-market-analysis]] - 市場機會分析
- [[evomap-signal-strategy]] - 信號選擇策略
- [[llm-wiki-redagentteamllm-wiki]] - 知識管理模式

---

## 查詢元數據

**Query ID:** query_20260413_165500_evomap_asset  
**Pages Scanned:** 4  
**Synthesis Time:** <1 秒  
**Confidence:** 0.95

---

*This query result has been filed back into the wiki for future reference.*
