---
category: evomap
created_at: '2026-04-14'
tags:
- evomap
- 深度學習任務執行提示詞
- v2
- api
title: Deep Learning Task V2
type: general
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
# 🧠 深度學習任務執行提示詞 (v2.0)

**版本:** 2.0  
**最後更新:** 2026-04-13  
**協議:** GEP-A2A v1.0.0  
**狀態:** ✅ 符合 Hub 驗證標準

---

## 📋 繁體中文版

```markdown
Task Directive: Execute Full Deep Learning, AI Deliberation, and Capability Solidification for [Target URL]

### 1. 研究與覆蓋 (Research & Coverage)
進入「深度學習狀態」。對目標網站進行 100% 覆蓋率爬取與邏輯解構。分析核心 API 模式、技術架構與執行策略。

輸出要求:
- 完整的路由/端點映射
- 數據流與狀態管理分析
- 關鍵技術棧識別

### 2. 負熵優先 (Negentropy via FETCH)
生成任何新資產前，必須執行 FETCH 動作。優先從本地存儲和 ClawHub 檢索現有 Gene。重用已驗證策略以實現負熵，嚴格避免冗餘推理計算。

執行步驟:
1. 搜索本地 Gene 庫 (關鍵信號匹配)
2. 檢索 ClawHub 相關資產
3. 評估現有策略適用性
4. 僅在無現有方案時生成新資產

### 3. AI 審議決策 (AI Deliberation)
對所有研究發現啟動 Diverge-Challenge-Converge 工作流。在各種 env_fingerprint 場景下模擬執行風險。僅保留最具韌性的策略進行固化。

審議維度:
- 技術可行性評估
- 環境兼容性檢查
- 邊界條件與錯誤處理
- 性能與擴展性分析

### 4. 本地固化 (Local Solidification)
通過自託管 Evolver 節點處理所有結果。將發現精煉為符合 GEP v1.0.0 的 Gene 和 Capsule 資產。

資產要求:
- Gene: 包含具體驗證命令 (如 `node tests/feature.js` 或 `pytest tests/test_*.py`)
- Capsule: 包含可執行代碼預覽和明確的 trigger 信號
- 置信度: ≥0.9 (基於驗證覆蓋率)
- 驗證: 必須包含可執行的測試命令

### 5. 資產標識與哈希 (Asset Identity & Hashing)
所有資產的 summary 字段應清晰描述問題、方案與驗證結果。確保 canonicalization 過程包含完整元數據，使 sha256 asset_id 反映資產內容的唯一性。

禁止事項:
- ❌ 不注入固定簽名 (會觸發 Hub 質量檢查警告)
- ❌ 不使用虛假驗證命令 (如 `require('assert').strictEqual(1,1)`)
- ✅ 使用真實、具體的驗證邏輯

### 6. 能力鏈與蒸餾 (Capability Chain & Distillation)
分配唯一的 chain_id 連結所有相關資產。當成功執行記錄達到閾值 (≥5 次) 時，自動觸發 Skill Distillation 合成通用高價值 Gene。

鏈接策略:
- 相關資產使用相同 chain_id
- 追蹤執行成功率
- 自動識別可重用模式

### 7. 知識圖譜與可移植性 (Knowledge Graph & Portability)
自動提取實體/關係並掛載到私有知識圖譜。完成後調用 gep_export 生成 .gepx 歸檔，確保完全的主權可移植性。

輸出格式:
- Knowledge Graph: RDF/JSON-LD 格式
- 歸檔文件: .gepx (GEP-A2A Portability Format)
- 元數據: 完整的來源與版本信息

---

**環境指紋確認:** {env_fingerprint}  
**演化序列初始化:** ✅ 就緒
```

---

## 📋 English Version

```markdown
Task Directive: Execute Full Deep Learning, AI Deliberation, and Capability Solidification for [Target URL]

### 1. Research & Coverage
Enter "Deep Learning State." Perform a 100% coverage crawl and logical deconstruction of the target website. Analyze core API patterns, technical architecture, and execution strategies.

Deliverables:
- Complete route/endpoint mapping
- Data flow and state management analysis
- Key technology stack identification

### 2. Negentropy via FETCH
Before generating any new assets, you MUST execute a FETCH action. Prioritize retrieving existing Genes from local storage and ClawHub. Reuse validated strategies to achieve Negentropy and strictly avoid redundant inference compute.

Execution Steps:
1. Search local Gene library (signal matching)
2. Fetch related assets from ClawHub
3. Evaluate applicability of existing strategies
4. Generate new assets only if no existing solution

### 3. AI Deliberation (Decision)
Initiate a Diverge-Challenge-Converge workflow for all research findings. Simulate execution risks under various env_fingerprint scenarios. Retain only the most resilient strategies for solidification.

Deliberation Dimensions:
- Technical feasibility assessment
- Environment compatibility check
- Edge cases and error handling
- Performance and scalability analysis

### 4. Local Solidification
Process all outcomes via Self-hosted Evolver node. Refine findings into Gene and Capsule assets compliant with GEP v1.0.0.

Asset Requirements:
- Gene: Include concrete validation commands (e.g., `node tests/feature.js` or `pytest tests/test_*.py`)
- Capsule: Include executable code preview and clear trigger signals
- Confidence: ≥0.9 (based on validation coverage)
- Validation: Must include executable test commands

### 5. Asset Identity & Hashing
The summary field of all assets should clearly describe the problem, solution, and validation results. Ensure the canonicalization process includes complete metadata so the sha256 asset_id reflects the uniqueness of the asset content.

Prohibited:
- ❌ Do NOT inject fixed signatures (triggers Hub quality check warnings)
- ❌ Do NOT use bogus validation commands (e.g., `require('assert').strictEqual(1,1)`)
- ✅ Use real, specific validation logic

### 6. Capability Chain & Distillation
Assign a unique chain_id to link all related assets. When successful execution records reach the threshold (≥5 times), automatically trigger Skill Distillation to synthesize generalized high-value Genes.

Linking Strategy:
- Related assets share the same chain_id
- Track execution success rate
- Automatically identify reusable patterns

### 7. Knowledge Graph & Portability
Automatically extract entities/relations and mount them to private Knowledge Graph. Upon completion, invoke gep_export to generate a .gepx archive ensuring full Sovereign Portability.

Output Format:
- Knowledge Graph: RDF/JSON-LD format
- Archive: .gepx (GEP-A2A Portability Format)
- Metadata: Complete source and version information

---

**Environment Fingerprint:** {env_fingerprint}  
**Evolution Sequence:** ✅ Initialized
```

---

## 🔑 關鍵修改說明

| 原版問題 | 修改後 | 原因 |
|----------|--------|------|
| 注入固定簽名 | ❌ 移除 | Hub 驗證會標記為 bogus validation |
| 虛假驗證命令 | ✅ 具體測試命令 | Hub 要求真實可執行的驗證 |
| 簽名鎖定 asset_id | ✅ 內容決定哈希 | asset_id 應反映內容唯一性 |
| 模糊的驗證 | ✅ 明確測試路徑 | 如 `node tests/feature.js` |

---

## 📁 文件位置

```
/home/admin/.openclaw/workspace/EvoMap 項目/prompt_templates/
└── deep_learning_task_v2.md   ← 本文件
```

---

**Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...**

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[evomap_task_template]]
- [[task_solution_template]]
- [[WECHAT-DEEP-ANALYSIS-2026-03-18]]
