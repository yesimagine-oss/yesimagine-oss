---
category: concept
created_at: '2026-04-14'
tags:
- concept
- auto-generated
title: Knowledge Files Complete List
type: concept
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
# LLM-Wiki 知識文件完整清單

**掃描時間:** 2026-04-13T09:40:00+08:00  
**執行者:** RedOpenClaw

---

## 📊 文件統計

| 目錄 | 文件類型 | 數量 | 完整路徑 |
|------|----------|------|----------|
| **源目錄** | Markdown | 19 | `/home/admin/llm-wiki/` |
| **目標目錄** | Markdown | 46 | `/home/admin/.openclaw/workspace/llm-wiki/` |
| **Skills 目錄** | SKILL.md | 32 | `/home/admin/.openclaw/workspace/skills/` |
| **Gene 文件** | JSON | 95 | `/home/admin/.openclaw/workspace/` |

---

## 📂 LLM-Wiki 目錄完整文件列表

### 源目錄 `/home/admin/llm-wiki/` (19 個文件)

```
/home/admin/llm-wiki/
├── AGENTS.md
├── CLAUDE.md
├── index.md
├── log.md
├── raw/
│   ├── asset01_docker_layer_cache.md
│   ├── asset02_k8s_healthcheck.md
│   ├── asset03_sql_n1_fix.md
│   ├── asset04_service_storm_protect.md
│   ├── asset05_task_solution_template.md
│   ├── asset06_k8s_resource_limit.md
│   └── asset07_api_batch_optimize.md
└── wiki/
    ├── api_batch_optimize.md
    ├── docker_layer_cache.md
    ├── evomap_task_template.md
    ├── k8s_healthcheck.md
    ├── k8s_resource_limit.md
    ├── service_storm_protect.md
    ├── sql_n1_fix.md
    └── taocan_demo.md
```

### 目標目錄 `/home/admin/.openclaw/workspace/llm-wiki/` (46 個文件)

```
/home/admin/.openclaw/workspace/llm-wiki/
├── AGENTS.md
├── CLAUDE.md
├── full-integration-report-20260413.md
├── index.md
├── log.md
├── merge-report-20260413.md
├── wiki-merge-report-20260413.md
├── raw/                    (11 個文件)
├── raw/raw/                (7 個文件)
└── raw/wiki/               (8 個文件)
└── wiki/                   (13 個文件)
```

---

## ❓「之前的 100+ 個去哪了？」

### 真相解析

**`index.md` 中的「100 項技能目錄」不是實際文件！**

這是一個**技能名稱索引/目錄**，列出了：
- Docker 構建優化（15 項）
- SQL 性能優化（15 項）
- K8s & 雲原生（15 項）
- API & 後端接口（12 項）
- OpenClaw 環境修復（10 項）
- EvoMap 增益工具（8 項）
- 代碼質量優化（10 項）
- 系統運維工具（5 項）
- 安全加固（4 項）
- AI 智能體增強（5 項）

**總計：99 項技能名稱**

這些是：
1. **技能的目錄/索引**，不是實際文件
2. 基於 **7 個原始資產** 蒸餾生成的**技能列表**
3. 用於 Agent 查找可用技能的**參考目錄**

### 實際文件 vs 技能目錄

| 類型 | 數量 | 說明 |
|------|------|------|
| **實際 Markdown 文件** | 19 | 真實存在的知識文件 |
| **技能目錄項** | ~100 | index.md 中列出的技能名稱 |
| **Skills 目錄文件** | 32 | `/home/admin/.openclaw/workspace/skills/` 中的 SKILL.md |
| **Gene 文件** | 95 | 蒸餾後的 Gene 資產 (JSON 格式) |

---

## 🔍 100+ 技能的實際位置

### 1. Skills 目錄 (32 個 SKILL.md)

```bash
/home/admin/.openclaw/workspace/skills/
├── adaptive-load-balancer/SKILL.md
├── agent-browser/SKILL.md
├── clipboard-manager/SKILL.md
├── content-collector/SKILL.md
├── evolver/SKILL.md
├── feishu-evolver-wrapper/SKILL.md
├── find-skills/SKILL.md
├── proactive-agent/SKILL.md
├── searxng/SKILL.md
├── self-improving-agent/SKILL.md
└── ... (共 32 個)
```

### 2. Gene 文件 (95 個)

```bash
/home/admin/.openclaw/workspace/gene_*.json
# 例如：
# gene_distilled_go_tooling_v1.json
# gene_distilled_hermes_deployment_v1.json
# gene_distilled_openclaw_core_architecture_v1.json
# ... (共 95 個)
```

### 3. EvoMap 資產

```bash
/home/admin/.openclaw/workspace/ai 知识变现/evomap 项目/evolver/assets/gep/genes.jsonl
```

---

## 📋 總結

**「100+ 個知識文件」從未以 Markdown 形式存在於 llm-wiki 目錄中！**

- **llm-wiki/** 包含的是 **7 個原始資產** 及其衍生的 **19 個 Markdown 文件**
- **100 項技能** 是 index.md 中的**目錄列表**，不是實際文件
- **實際技能實現** 位於：
  - `/home/admin/.openclaw/workspace/skills/` (32 個 SKILL.md)
  - `/home/admin/.openclaw/workspace/gene_*.json` (95 個 Gene 文件)

---

## ✅ 驗證命令

```bash
# 檢查 llm-wiki 實際文件
find /home/admin/llm-wiki/ -type f -name "*.md" | wc -l
# 結果：19

# 檢查目標目錄實際文件
find /home/admin/.openclaw/workspace/llm-wiki/ -type f -name "*.md" | wc -l
# 結果：46

# 檢查 Skills 目錄
find /home/admin/.openclaw/workspace/skills/ -name "SKILL.md" | wc -l
# 結果：32

# 檢查 Gene 文件
find /home/admin/.openclaw/workspace/ -name "gene_*.json" | wc -l
# 結果：95
```

---

**報告生成時間:** 2026-04-13T09:40:00+08:00

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[ULTIMATE-COMPLETE-REPORT]]
- [[07-evomap_knowledge_merge]]
- [[15-gene_distilled_go_knowledge_ingest]]
