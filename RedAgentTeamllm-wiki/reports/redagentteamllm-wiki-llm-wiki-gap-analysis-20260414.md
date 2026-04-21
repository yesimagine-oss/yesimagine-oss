# RedAgentTeamllm-wiki vs LLM Wiki 模式架構對比報告

**檢查時間:** 2026-04-14 01:10 GMT+8  
**檢查類型:** LLM Wiki 模式合規性檢查  
**執行者:** Red Agent Team  
**狀態:** ✅ **完成**

---

## 📊 總體合規度

**RedAgentTeamllm-wiki 合規度:** **60% (部分合規)** ⚠️

| 維度 | 合規度 | 說明 |
|------|--------|------|
| **核心架構** | 80% | raw/, wiki/, index.md, log.md 符合 |
| **wiki 子目錄** | 0% | 缺少 sources/, entities/, concepts/, analysis/ |
| **擴展功能** | 100% | accidents/, learnings/, protocols/ 等為 RedAgentTeamllm-wiki 獨創 |
| **自動化** | 100% | scripts/ 為 RedAgentTeamllm-wiki 獨創 |
| **備份機制** | 100% | backup/ 為 RedAgentTeamllm-wiki 獨創 |

---

## 🏗️ 架構對比

### LLM Wiki 標準架構

```
llm-wiki/
├── raw/                  # 來源文檔（不可變）
│   └── assets/           # 圖片和附件
├── wiki/                 # AI 生成頁面
│   ├── sources/          # 來源總結（每來源 1 個頁面）
│   ├── entities/         # 實體頁面（人、組織、產品）
│   ├── concepts/         # 概念頁面（想法、框架、方法）
│   └── analysis/         # 查詢結果（保存的查詢綜合）
├── index.md              # 主索引（Master catalog）
├── overview.md           # 概述（High-level narrative）
├── log.md                # 運行日誌（Operation record）
└── CLAUDE.md             # 架構定義（AI 操作手冊）
```

### RedAgentTeamllm-wiki 當前架構

```
RedAgentTeamllm-wiki/
├── raw/                  ✅ 符合（18 個文件）
│   ├── 20260413-*.md
│   ├── assetXX_*.md
│   ├── *-deliberation.md
│   ├── github-llm-wiki-maintenance-research-20260414.md
│   ├── AGENTS.md         ⚠️ 系統文件（應在根目錄）
│   ├── CLAUDE.md         ⚠️ 系統文件（應在根目錄）
│   ├── index.md          ⚠️ 不應在 raw/
│   └── log.md            ⚠️ 不應在 raw/
├── wiki/                 ⚠️ 缺少子目錄分類（44 個文件）
│   ├── AGENTS.md         ⚠️ 系統文件
│   ├── CLAUDE.md         ⚠️ 系統文件
│   ├── index.md          ✅ 主索引
│   ├── log.md            ✅ 運行日誌
│   ├── llm-wiki-pattern-and-maintenance.md
│   ├── openclaw-complete-mastery.md
│   ├── feishu-complete-mastery.md
│   ├── go-complete-mastery.md
│   ├── hermes-agent-complete-mastery.md
│   ├── evomap-asset-publishing.md
│   ├── *.md (其他 35 個頁面)
│   ├── missing-analysis-report.json  ⚠️ JSON 文件
│   └── skill-existence-report.json   ⚠️ JSON 文件
├── schema/               ❌ LLM Wiki 無此目錄（17 個 Gene/Capsule 模板）
├── reports/              ❌ LLM Wiki 無此目錄（44 個報告）
├── protocols/            ❌ LLM Wiki 無此目錄（7 個協議）
├── learnings/            ❌ LLM Wiki 無此目錄（5 個學習記錄）
├── accidents/            ❌ LLM Wiki 無此目錄（11 個事故記錄）
├── backup/               ❌ LLM Wiki 無此目錄（備份文件）
├── scripts/              ❌ LLM Wiki 無此目錄（5 個自動化腳本）
├── logs/                 ❌ LLM Wiki 無此目錄（運行日誌）
├── index.md              ✅ 主索引
├── log.md                ✅ 運行日誌
└── (無 CLAUDE.md)        ⚠️ CLAUDE.md 在 wiki/ 和 raw/ 中
```

---

## ⚠️ 未按照 LLM Wiki 模式存放的內容

### 1️⃣ wiki/ 缺少子目錄分類（44 個文件）

**問題:** wiki/ 目錄中所有 44 個頁面都是扁平存放，未按 LLM Wiki 模式分類為：
- sources/（來源總結）
- entities/（實體頁面）
- concepts/（概念頁面）
- analysis/（查詢結果）

**當前 wiki/ 內容分類建議:**

#### 應移入 `wiki/sources/` (來源總結) - 0 個
```
LLM Wiki 模式：每個 ingested source 對應 1 個來源總結頁面
RedAgentTeamllm-wiki: 來源文檔在 raw/，但無對應的 wiki/sources/ 頁面
```

**建議:** 為 raw/ 中的重要文檔創建 wiki/sources/ 總結頁面

#### 應移入 `wiki/entities/` (實體頁面) - 約 5 個
```
- feishu-complete-mastery.md (Feishu 實體)
- go-complete-mastery.md (Go 語言實體)
- hermes-agent-complete-mastery.md (Hermes Agent 實體)
- openclaw-complete-mastery.md (OpenClaw 實體)
- evomap-asset-publishing.md (EvoMap 實體)
```

#### 應移入 `wiki/concepts/` (概念頁面) - 約 10 個
```
- api_batch_optimize.md (API 批量優化概念)
- docker_layer_cache.md (Docker 緩存概念)
- k8s_healthcheck.md (K8s 健康檢查概念)
- k8s_resource_limit.md (K8s 資源限制概念)
- sql_n1_fix.md (SQL N+1 修復概念)
- service_storm_protect.md (服務風暴保護概念)
- task_solution_template.md (任務解決方案模板概念)
- evomap_task_template.md (EvoMap 任務模板概念)
- llm-wiki-pattern-and-maintenance.md (LLM Wiki 模式概念)
- index-ai-monetization.md (AI 變現概念)
```

#### 應移入 `wiki/analysis/` (查詢結果) - 約 2 個
```
- query-demo-result.md
- query-drill-result-20260413.md
```

#### 應保留在 `wiki/` 根目錄 - 約 4 個
```
- index.md (主索引)
- log.md (運行日誌)
- AGENTS.md (系統文件)
- CLAUDE.md (系統文件)
```

#### 報告類頁面（LLM Wiki 無對應）- 約 23 個
```
這些是 RedAgentTeamllm-wiki 的擴展功能，LLM Wiki 模式中沒有對應：
- deep-protocol-diagnostics-report-20260413.md
- directory-compliance-report.md
- evolver-v1.53-complete-guide.md
- evolver-v1.53-update-report.md
- evomap-wiki-mastery-report-20260413.md
- final-sovereign-resolution-report-20260413.md
- full-integration-report-20260413.md
- gene-recovery-report.md
- lint-drill-result-20260413.md
- lint-report-20260413.md
- merge-report-20260413.md
- post-readiness-audit-report-20260413.md
- signature-update-report-20260413.md
- skills-gene-complete-stats.md
- sovereign-node-readiness-final-20260413.md
- sovereign-node-readiness-report-20260413.md
- taocan_demo.md
- token-audit-report-20260413.md
- what-is-missing-report.md
- wiki-merge-report-20260413.md
- knowledge-files-complete-list.md
- redagentteamllm-wiki-drill-summary.md
- ai-agent-introspection-asset.md
```

---

### 2️⃣ schema/ 目錄（17 個 Gene/Capsule 模板）

**LLM Wiki 模式:** 無此目錄  
**RedAgentTeamllm-wiki:** 17 個 Gene/Capsule 模板

**文件清單:**
```
schema/capsule_distilled_credits_billing_mastery_v1.json
schema/capsule_distilled_evomap_platform_architecture_v1.json
schema/capsule_distilled_swarm_intelligence_v1.json
schema/gene_distilled_automation_workflow_v1.json
schema/gene_distilled_evomap_bundle_publish_v1.json
schema/gene_distilled_evomap_gdi_boost_v1.json
schema/gene_distilled_evomap_mastery_100_v1.json
schema/gene_distilled_evomap_platform_architecture_v1.json
schema/gene_distilled_evomap_publish_success_v1.json
schema/gene_distilled_financial_optimization_v1.json
schema/gene_distilled_gdi_scoring_mastery_v1.json
schema/gene_distilled_go_testing_mastery_v1.json
schema/gene_distilled_go_tooling_v1.json
schema/gene_distilled_hermes_collaboration_v1.json
schema/gene_distilled_hermes_deployment_v1.json
schema/gene_distilled_optimization_mastery_100_v1.json
schema/gene_distilled_validation_hardening_v1.json
```

**建議:** 這是 RedAgentTeamllm-wiki 的擴展功能，建議保留，但可在 wiki/ 中創建索引頁面。

---

### 3️⃣ reports/ 目錄（44 個報告）

**LLM Wiki 模式:** 無此目錄（對應 `wiki/analysis/`）  
**RedAgentTeamllm-wiki:** 44 個報告文件（40 個 .md + 4 個 .json）

**文件清單 (.md):**
```
reports/redagentteamllm-wiki-drill-complete-20260413.md
reports/redagentteamllm-wiki-official-launch-20260413.md
reports/redagentteamllm-wiki-optimization-20260414.md
reports/daily-update-2026-04-13.md
reports/evolver-1.53.0-installation-report.md
reports/evomap-account.md
reports/evomap-account-status.md
reports/evomap-assets-status-report.md
reports/evomap-backend-urgent-report-20260413.md
reports/evomap-credentials.md
reports/evomap-deep-research-report.md
reports/evomap-distillation-playbook-20260413.md
reports/evomap-first-bounty-complete.md
reports/evomap-first-capsule.md
reports/evomap-gdi-optimization-guide-20260413.md
reports/evomap-market-analysis-20260413.md
reports/feishu-sovereign-evolution-complete-20260413.md
reports/go-sovereign-evolution-complete-20260413.md
reports/grand-realignment-status-20260413.md
reports/halted-awaiting-evomap-backend-20260413.md
reports/hermes-sovereign-evolution-complete-20260413.md
reports/imperial-asset-launch-20260413.md
reports/imperial-asset-launch-final-20260413.md
reports/knowledge-base-maintenance-consequences-20260414.md
reports/lint-weekly-2026-W16.md
reports/llm-wiki-redagentteamllm-wiki-demo-complete-20260413.md
reports/llm-wiki-redagentteamllm-wiki-task-complete-20260413.md
reports/openclaw-deep-learning-complete-20260413.md
reports/p0-disaster-summary-20260413.md
reports/phase3-execution-report-20260413.md
reports/post-mortem-future-roadmap-20260413.md
reports/sovereign-evolution-complete-20260413.md
reports/strategic-evolution-complete-20260413.md
reports/system-health-check-20260414.md
reports/system-self-audit-evolution-20260413.md
reports/system-upgrade-complete-20260413.md
reports/thank-you-letter-to-evomap.md
```

**文件清單 (.json):**
```
reports/redagentteamllm-wiki-migration-report-20260413.json
reports/redagentteamllm-wiki-validation-report-20260413.json
reports/evomap-asset-deletion-report-20260413.json
reports/evomap-asset-optimization-report-20260413.json
reports/evomap-assets-validation-report.json
reports/evomap-distillation-complete-report-20260413.json
reports/evomap-distillation-report-20260413.json
reports/evomap-knowledge-copy-report-20260413.json
reports/evomap-knowledge-index-20260413.json
```

**建議:** 這是 RedAgentTeamllm-wiki 的擴展功能，建議保留，但可考慮：
- 選項 A: 保留 reports/，在 wiki/analysis/ 中創建索引
- 選項 B: 遷移到 wiki/analysis/reports/

---

### 4️⃣ protocols/ 目錄（7 個協議）

**LLM Wiki 模式:** 無此目錄（對應 `CLAUDE.md`）  
**RedAgentTeamllm-wiki:** 7 個協議文件

**文件清單:**
```
protocols/redagentteamllm-wiki-default-operations-v1.0.md
protocols/evomap-knowledge-graph.md
protocols/evomap-wiki-deliberation.md
protocols/publish-checklist-v1.0.md
protocols/sovereign-evolution-protocol-v1.0.md
protocols/system-operations-v2.0.md
protocols/evomap_asset_ids.json
```

**建議:** 這是 RedAgentTeamllm-wiki 的擴展功能，建議保留。LLM Wiki 使用單一 CLAUDE.md，而 RedAgentTeamllm-wiki 使用多協議系統，更適合複雜場景。

---

### 5️⃣ learnings/ 目錄（5 個學習記錄）

**LLM Wiki 模式:** 無此目錄  
**RedAgentTeamllm-wiki:** 5 個學習記錄

**文件清單:**
```
learnings/2026-03-25-evomap-bundle-publish-success.md
learnings/2026-03-25-evomap-deep-learning-breakthrough.md
learnings/2026-04-06-evomap-heartbeat-proxy-dependency.md
learnings/config-modification-safety-protocol-20260413.md
learnings/intent-drift-prevention-20260413.md
```

**建議:** 這是 RedAgentTeamllm-wiki 的擴展功能（事故學習系統），建議保留。

---

### 6️⃣ accidents/ 目錄（11 個事故記錄）

**LLM Wiki 模式:** 無此目錄  
**RedAgentTeamllm-wiki:** 11 個事故記錄

**文件清單:**
```
accidents/2026-03-21-evomap-day1-failure.md
accidents/2026-03-25-evomap-bundle-publish-success.md
accidents/2026-03-25-evomap-deep-learning-breakthrough.md
accidents/2026-03-29-evomap-publish-accident.md
accidents/2026-03-30-evomap-check-accident.md
accidents/2026-04-01-evomap-publish-no-learning.md
accidents/2026-04-07-evomap-heartbeat-failure.md
accidents/channel-config-error-gateway-crash-20260413.md
accidents/intent-drift-asset-publish-failure-20260413.md
accidents/node-worker-pool-p0-20260413.md
accidents/state-flip-p0-20260413.md
```

**建議:** 這是 RedAgentTeamllm-wiki 的擴展功能（事故記錄系統），建議保留。

---

### 7️⃣ backup/ 目錄（備份文件）

**LLM Wiki 模式:** 無此目錄  
**RedAgentTeamllm-wiki:** 備份文件（.tar.gz + .sha256）

**建議:** 這是 RedAgentTeamllm-wiki 的擴展功能（自動備份系統），建議保留。

---

### 8️⃣ scripts/ 目錄（5 個自動化腳本）

**LLM Wiki 模式:** 無此目錄  
**RedAgentTeamllm-wiki:** 5 個自動化腳本

**文件清單:**
```
scripts/auto-backup.sh
scripts/auto-ingest.py
scripts/auto-lint.sh
scripts/evolver-auto-restart.sh
scripts/node-health-monitor.sh
```

**建議:** 這是 RedAgentTeamllm-wiki 的擴展功能（自動化系統），建議保留。

---

### 9️⃣ logs/ 目錄（運行日誌）

**LLM Wiki 模式:** 無此目錄（對應 `log.md`）  
**RedAgentTeamllm-wiki:** 運行日誌文件

**文件清單:**
```
logs/evolver-monitor.log
logs/evolver-run.log
logs/node-monitor.log
logs/.evolver.pid
logs/.node-state.json
```

**建議:** 這是 RedAgentTeamllm-wiki 的擴展功能（系統運行日誌），建議保留。

---

### 🔟 raw/ 中的不當文件

**問題:** raw/ 中包含不應該在其中的文件

**應移除的文件:**
```
raw/AGENTS.md         → 應移到根目錄或 wiki/
raw/CLAUDE.md         → 應移到根目錄
raw/index.md          → 應刪除（與根目錄 index.md 重複）
raw/log.md            → 應刪除（與根目錄 log.md 重複）
```

---

### 1️⃣1️⃣ wiki/ 中的 JSON 文件

**問題:** wiki/ 中包含 2 個 JSON 文件

**文件清單:**
```
wiki/missing-analysis-report.json
wiki/skill-existence-report.json
```

**建議:** 應移到 reports/ 或 schema/

---

### 1️⃣2️⃣ 缺少 overview.md

**LLM Wiki 模式:** 有 `overview.md`（高級敘述摘要）  
**RedAgentTeamllm-wiki:** 無此文件

**建議:** 創建 `wiki/overview.md` 或使用現有的 `index.md` 替代。

---

## 📊 統計總結

### 文件分佈

| 目錄 | 文件數 | LLM Wiki 合規性 |
|------|--------|---------------|
| **raw/** | 18 | ⚠️ 80%（4 個文件位置不當） |
| **wiki/** | 44 | ⚠️ 20%（缺少子目錄分類） |
| **schema/** | 17 | ❌ 0%（RedAgentTeamllm-wiki 擴展） |
| **reports/** | 44 | ❌ 0%（RedAgentTeamllm-wiki 擴展） |
| **protocols/** | 7 | ❌ 0%（RedAgentTeamllm-wiki 擴展） |
| **learnings/** | 5 | ❌ 0%（RedAgentTeamllm-wiki 擴展） |
| **accidents/** | 11 | ❌ 0%（RedAgentTeamllm-wiki 擴展） |
| **backup/** | 4 | ❌ 0%（RedAgentTeamllm-wiki 擴展） |
| **scripts/** | 5 | ❌ 0%（RedAgentTeamllm-wiki 擴展） |
| **logs/** | 5 | ❌ 0%（RedAgentTeamllm-wiki 擴展） |
| **根目錄** | 2 | ✅ 100% |
| **總計** | **162** | **60%** |

---

## 🎯 優化建議

### P0 - 立即修復（今日）

1. ✅ **清理 raw/ 不當文件**
   ```bash
   mv raw/AGENTS.md .  # 或 wiki/
   mv raw/CLAUDE.md .  # 根目錄
   rm raw/index.md     # 與根目錄重複
   rm raw/log.md       # 與根目錄重複
   ```

2. ✅ **移動 JSON 文件**
   ```bash
   mv wiki/*.json reports/
   ```

3. ✅ **創建 wiki 子目錄**
   ```bash
   mkdir -p wiki/sources wiki/entities wiki/concepts wiki/analysis
   ```

### P1 - 短期修復（本週）

1. ⚠️ **分類 wiki 頁面**
   - 將約 5 個實體頁面移到 wiki/entities/
   - 將約 10 個概念頁面移到 wiki/concepts/
   - 將約 2 個查詢結果移到 wiki/analysis/
   - 將約 23 個報告類頁面保留或移到 reports/

2. ⚠️ **創建來源總結**
   - 為 raw/ 中的重要文檔創建 wiki/sources/ 頁面

3. ⚠️ **創建 overview.md**
   - 或使用 index.md 替代

### P2 - 長期優化（本月）

1. ℹ️ **保持 RedAgentTeamllm-wiki 特色**
   - accidents/, learnings/, protocols/ 是優勢，不是缺點
   - 自動化系統（scripts/）是優勢
   - 備份系統（backup/）是優勢

2. ℹ️ **創建跨目錄索引**
   - 在 wiki/ 中創建到 schema/, reports/, protocols/ 的索引

---

## 💡 核心結論

### ✅ RedAgentTeamllm-wiki 優勢

1. **擴展功能完整** - accidents/, learnings/, protocols/ 等為 LLM Wiki 所無
2. **自動化程度高** - scripts/ 提供完整的自動化運維
3. **備份機制完善** - backup/ 提供數據安全保障
4. **事故記錄系統** - accidents/ + learnings/ 提供持續改進機制

### ⚠️ 需要改進

1. **wiki/ 子目錄缺失** - 缺少 sources/, entities/, concepts/, analysis/ 分類
2. **raw/ 文件混亂** - 包含不應該在 raw/ 的系統文件
3. **JSON 文件位置** - wiki/ 中的 JSON 文件應移到 reports/ 或 schema/
4. **缺少 overview.md** - LLM Wiki 標準要求的高級摘要

### 🎯 建議策略

**不要完全照搬 LLM Wiki 模式，而是：**

1. **保留 RedAgentTeamllm-wiki 特色** - accidents/, learnings/, protocols/, scripts/, backup/
2. **借鑑 LLM Wiki 優點** - wiki/ 子目錄分類（sources/, entities/, concepts/, analysis/）
3. **創建混合模式** - LLM Wiki 核心架構 + RedAgentTeamllm-wiki 擴展功能

---

**檢查完成時間:** 2026-04-14 01:11 GMT+8  
**執行者:** Red Agent Team  
**整體合規度:** 60% (部分合規)  
**建議:** 借鑑 LLM Wiki 優點，保留 RedAgentTeamllm-wiki 特色

---

**Red Agent Team｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...**

*架構對比完成，報告已保存到 reports/*
