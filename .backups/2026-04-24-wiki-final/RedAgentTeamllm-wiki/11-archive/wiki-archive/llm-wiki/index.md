---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Index
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
# LLM Wiki 全局索引 · Global Index

**版本**: 2.0.0 (Karpathy 架構)  
**最後更新**: 2026-04-17 06:00 GMT+8  
**維護者**: LLM (AI Agent)  
**人類權限**: 只讀

---

## 📋 索引規範

### 分層結構
```
llm-wiki/
├── index.md            # 全局索引 (本文件)
├── raw/
│   └── index.md        # Raw 層索引 (原始資料目錄)
├── wiki/
│   └── index.md        # Wiki 層索引 (知識條目索引)
├── genes/
│   └── index.md        # Genes 層索引 (規則基因索引)
└── capsules/
    └── index.md        # Capsules 層索引 (實例膠囊索引)
```

### 索引格式
```markdown
## 分類名稱

| 名稱 | 類型 | 創建日期 | 狀態 | 標籤 |
|------|------|----------|------|------|
| 文件名 | Gene/Capsule/知識 | YYYY-MM-DD | ✅ Active | #tag1 #tag2 |
```

---

## 📊 統計

| 層級 | 文件數 | 最後更新 |
|------|--------|----------|
| **全局** | 1 | 2026-04-17 |
| Raw 層 | ~15 | 2026-04-17 |
| Wiki 層 | ~50 | 2026-04-17 |
| Genes 層 | 25 (8 Karpathy + 17 Ollama) | 2026-04-17 |
| Capsules 層 | 7 (Ollama) | 2026-04-17 |
| **總計** | **~98** | **2026-04-17** |

---

## 🧬 Genes 層索引

### Karpathy 核心 Genes (8 個)

| Gene ID | 名稱 | 創建日期 | 狀態 | 標籤 |
|---------|------|----------|------|------|
| GENE_001 | Karpathy Core Ideal | 2026-04-17 | ✅ Active | #AOT #knowledge_compilation |
| GENE_002 | Three Layer Architecture | 2026-04-17 | ✅ Active | #architecture #Raw #Wiki #Schema |
| GENE_003 | Ingest Workflow | 2026-04-17 | ✅ Active | #workflow #compilation |
| GENE_004 | Query Workflow | 2026-04-17 | ✅ Active | #workflow #query #沉淀 |
| GENE_005 | Lint Workflow | 2026-04-17 | ✅ Active | #workflow #lint #health |
| GENE_006 | Human LLM Duty Separation | 2026-04-17 | ✅ Active | #duty #separation |
| GENE_007 | Markdown Git Native | 2026-04-17 | ✅ Active | #markdown #git |
| GENE_008 | Schema Co-Evolution | 2026-04-17 | ✅ Active | #schema #evolution |

### Ollama Genes (17 個)

**位置**: `ollama/genes/`  
**詳情**: [ollama/INDEX.md](ollama/INDEX.md)

| Gene ID | 名稱 | 狀態 |
|---------|------|------|
| gene_ollama_install | Ollama 跨平台安裝 | ✅ Active |
| gene_ollama_start | Ollama 服務啟動 | ✅ Active |
| gene_ollama_pull | Ollama 模型拉取 | ✅ Active |
| gene_ollama_run | Ollama 模型運行 | ✅ Active |
| gene_ollama_list | Ollama 模型列表 | ✅ Active |
| gene_model_layer_build | 模型層構建 | ✅ Active |
| gene_model_quantize | 模型量化 | ✅ Active |
| gene_infer_text | 文本推理 | ✅ Active |
| gene_infer_multimodal | 多模態推理 | ✅ Active |
| gene_infer_stream | 流式推理 | ✅ Active |
| gene_tool_call_stream | 工具調用流式 | ✅ Active |
| gene_hardware_detect | 硬件檢測 | ✅ Active |
| gene_apple_silicon_optimize | Apple 矽優化 | ✅ Active |
| gene_cuda_optimize | CUDA 優化 | ✅ Active |
| gene_privacy_local_only | 隱私本地優先 | ✅ Active |
| gene_audit_log | 審計日志 | ✅ Active |
| gene_rag_local | 本地 RAG | ✅ Active |

**小計**: 25 Genes

---

## 📦 Capsules 層索引

### Ollama Capsules (7 個)

**位置**: `ollama/capsules/`  
**詳情**: [ollama/INDEX.md](ollama/INDEX.md)

| Capsule ID | 名稱 | 對應 Gene | 狀態 |
|-----------|------|----------|------|
| capsule_ollama_oneclick_deploy_v1 | Ollama 一鍵部署 | gene_ollama_install | ✅ Active |
| capsule_ollama_private_model_repo_v1 | 私有模型倉庫 | gene_ollama_pull | ✅ Active |
| capsule_ollama_multimodal_assistant_v1 | 多模態助手 | gene_infer_multimodal | ✅ Active |
| capsule_ollama_streaming_agent_v1 | 流式 Agent | gene_tool_call_stream | ✅ Active |
| capsule_ollama_apple_silicon_optimize_v1 | Apple 矽優化 | gene_apple_silicon_optimize | ✅ Active |
| capsule_ollama_enterprise_local_rag_v1 | 企業本地 RAG | gene_rag_local | ✅ Active |
| capsule_ollama_low_cpu_ai_v1 | 低 CPU AI | gene_cuda_optimize | ✅ Active |

**小計**: 7 Capsules

---

## 📚 Wiki 層索引

**位置**: `wiki/index.md`  
**詳情**: [wiki/index.md](wiki/index.md)

### 主要分類
- Docker 構建優化 (~15 項)
- SQL 性能優化 (~15 項)
- K8s & 雲原生 (~15 項)
- API 批量優化 (~10 項)
- 服務重啟防護 (~5 項)
- 其他 (~10 項)

**小計**: ~70 知識條目

---

## 📁 Raw 層索引

**位置**: `raw/index.md`  
**詳情**: [raw/index.md](raw/index.md)

### 原始資料
- 配置文件
- 參考文檔
- 源代碼片段

**小計**: ~15 原始文件

---

## 🔗 交叉引用

### 層級關係
```
Raw (人類輸入)
  ↓ Ingest
Wiki (編譯知識)
  ↑ Query
Genes (規則定義)
  ↓ 實例化
Capsules (可執行)
```

### 相關索引
- [ollama/INDEX.md](ollama/INDEX.md) - Ollama 專用索引
- [wiki/index.md](wiki/index.md) - Wiki 知識索引
- [raw/index.md](raw/index.md) - Raw 資料索引

---

## 📝 更新日志

| 日期 | 變更 | 執行者 |
|------|------|--------|
| 2026-04-17 | 統一為 Karpathy 分層索引 | LLM |
| 2026-04-13 | 合併所有知識文件 | RedOpenClaw |

---

**維護規範**: 詳見 [schema.md](schema.md)


## 相關文檔

- [[INDEX-ALL]]
- [[agentteam-index]]
- [[INDEX]]
