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
# Ollama 知識庫完整索引

**版本**: 2.0.0 (Karpathy 架構)  
**創建時間**: 2026-04-17 05:26 GMT+8  
**最後更新**: 2026-04-17 06:00 GMT+8  
**總資產**: 24 個 (17 Genes + 7 Capsules)

---

## 🔗 交叉引用

### 上級索引
- [../index.md](../index.md) - LLM Wiki 全局索引
- [../genes/](../genes/) - Karpathy 核心 Genes (8 個)

### 相關規範
- [../schema.md](../schema.md) - 核心操作規範
- [../genes/karpathy-core-ideal.gene.md](../genes/karpathy-core-ideal.gene.md) - AOT 編譯理念

### 下級執行
- [capsules/](capsules/) - 可執行 Capsules
- [genes/](genes/) - Ollama 專用 Genes

---

---

## 📊 統計總覽

| 類別 | Genes | Capsules | 總計 |
|------|-------|----------|------|
| 部署底座 | 2 | 1 | 3 |
| 模型管理 | 3 | 1 | 4 |
| 模型定制 | 2 | 0 | 2 |
| 推理引擎 | 3 | 2 | 5 |
| 硬件適配 | 3 | 2 | 5 |
| 安全合規 | 2 | 1 | 3 |
| 知識庫 | 1 | 0 | 1 |
| 普惠 AI | 0 | 1 | 1 |
| **總計** | **17** | **7** | **24** |

---

## 🧬 Genes 索引 (17 個)

### 部署底座 (2)

| ID | 名稱 | 置信度 | 說明 |
|----|------|--------|------|
| `gene_ollama_install` | Ollama 跨平台安裝 | 0.99 | macOS/Linux/Windows/Docker 一鍵安裝 |
| `gene_ollama_start` | Ollama 服務啟動 | 0.99 | 啟動 11434 端口後台服務 |

### 模型管理 (3)

| ID | 名稱 | 置信度 | 說明 |
|----|------|--------|------|
| `gene_ollama_pull` | 模型拉取 | 0.99 | 從官方庫拉取模型鏡像 |
| `gene_ollama_run` | 模型運行 | 0.99 | 交互/非交互模式運行模型 |
| `gene_ollama_list` | 本地模型列表 | 0.98 | 列出已安裝模型信息 |

### 模型定制 (2)

| ID | 名稱 | 置信度 | 說明 |
|----|------|--------|------|
| `gene_model_layer_build` | 模型分層構建 | 0.97 | 基礎層 + 量化層 + 定制層打包 |
| `gene_model_quantize` | 模型量化 | 0.98 | 4bit/8bit 量化降低顯存 |

### 推理引擎 (3)

| ID | 名稱 | 置信度 | 說明 |
|----|------|--------|------|
| `gene_infer_text` | 文本推理 | 0.99 | 文本生成、問答、摘要、翻譯 |
| `gene_infer_multimodal` | 多模態推理 | 0.96 | 圖文理解、視覺問答 |
| `gene_infer_stream` | 流式推理 | 0.99 | 逐 Token 流式輸出 |

### Agent 能力 (1)

| ID | 名稱 | 置信度 | 說明 |
|----|------|--------|------|
| `gene_tool_call_stream` | 流式工具調用 | 0.97 | 邊輸出邊執行工具調用 |

### 硬件適配 (3)

| ID | 名稱 | 置信度 | 說明 |
|----|------|--------|------|
| `gene_hardware_detect` | 硬件檢測 | 0.99 | CPU/GPU/內存/架構檢測 |
| `gene_apple_silicon_optimize` | Apple Silicon 優化 | 0.98 | Metal/MLX 加速 |
| `gene_cuda_optimize` | NVIDIA CUDA 優化 | 0.98 | CUDA 核函數調度優化 |

### 安全合規 (2)

| ID | 名稱 | 置信度 | 說明 |
|----|------|--------|------|
| `gene_privacy_local_only` | 本地隱私隔離 | 1.00 | 數據不上雲、本地閉環 |
| `gene_audit_log` | 操作審計日誌 | 0.99 | API 調用、模型訪問全記錄 |

### 知識庫 (1)

| ID | 名稱 | 置信度 | 說明 |
|----|------|--------|------|
| `gene_rag_local` | 本地 RAG 嵌入檢索 | 0.97 | 私有文檔嵌入 + 檢索 |

---

## 💊 Capsules 索引 (7 個)

### 基礎設施 (1)

| ID | 名稱 | 成功率 | 說明 |
|----|------|--------|------|
| `capsule_ollama_oneclick_deploy_v1` | Ollama 一鍵部署膠囊 | 0.99 | 5 分鐘搭建本地大模型服務 |

### 模型管理 (1)

| ID | 名稱 | 成功率 | 說明 |
|----|------|--------|------|
| `capsule_ollama_private_model_repo_v1` | 私有模型倉庫膠囊 | 0.97 | 分層存儲 + 版本管理 + 回滾 |

### AI 助手 (1)

| ID | 名稱 | 成功率 | 說明 |
|----|------|--------|------|
| `capsule_ollama_multimodal_assistant_v1` | 本地多模態助手膠囊 | 0.95 | 圖文理解 + 流式對話閉環 |

### Agent 自動化 (1)

| ID | 名稱 | 成功率 | 說明 |
|----|------|--------|------|
| `capsule_ollama_streaming_agent_v1` | 流式工具調用 Agent 膠囊 | 0.96 | 邊輸出邊執行工具，本地閉環 |

### 硬件優化 (1)

| ID | 名稱 | 成功率 | 說明 |
|----|------|--------|------|
| `capsule_ollama_apple_silicon_optimize_v1` | Apple Silicon 高性能膠囊 | 0.98 | MLX/Metal 極致加速 |

### 企業應用 (1)

| ID | 名稱 | 成功率 | 說明 |
|----|------|--------|------|
| `capsule_ollama_enterprise_local_rag_v1` | 企業本地隱私 RAG 膠囊 | 0.97 | 數據不出境 + 權限隔離 + 私有問答 |

### 普惠 AI (1)

| ID | 名稱 | 成功率 | 說明 |
|----|------|--------|------|
| `capsule_ollama_low_cpu_ai_v1` | 低配 CPU 本地 AI 膠囊 | 0.90 | 無 GPU 也可運行 7B 模型 |

---

## 🔗 依賴關係圖

```
ollama-install ─┬─> ollama-start ─> ollama-pull ─> ollama-run
                │
                └─> [oneclick-deploy]

model-layer-build ─> model-quantize ─> [private-model-repo]

infer-text ─┬─> infer-stream ─> tool-call-stream ─> [streaming-agent]
            │
            └─> infer-multimodal ─> [multimodal-assistant]

hardware-detect ─┬─> apple-silicon-optimize ─> [apple-silicon-optimize-capsule]
                 │
                 └─> cuda-optimize

privacy-local-only ─┬─> audit-log ─> [enterprise-local-rag]
                    │
                    └─> rag-local ──┘

model-quantize ─> [low-cpu-ai]
```

---

## 📁 文件路徑

### Genes

```
genes/ollama-install.gene.md
genes/ollama-start.gene.md
genes/ollama-pull.gene.md
genes/ollama-run.gene.md
genes/ollama-list.gene.md
genes/model-layer-build.gene.md
genes/model-quantize.gene.md
genes/infer-text.gene.md
genes/infer-multimodal.gene.md
genes/infer-stream.gene.md
genes/tool-call-stream.gene.md
genes/hardware-detect.gene.md
genes/apple-silicon-optimize.gene.md
genes/cuda-optimize.gene.md
genes/privacy-local-only.gene.md
genes/audit-log.gene.md
genes/rag-local.gene.md
```

### Capsules

```
capsules/ollama-oneclick-deploy.capsule.md
capsules/ollama-private-model-repo.capsule.md
capsules/ollama-multimodal-assistant.capsule.md
capsules/ollama-streaming-agent.capsule.md
capsules/ollama-apple-silicon-optimize.capsule.md
capsules/ollama-enterprise-local-rag.capsule.md
capsules/ollama-low-cpu-ai.capsule.md
```

---

## ✅ 合規狀態

| 檢查項 | 狀態 | 說明 |
|--------|------|------|
| schema_version | ✅ 1.5.0 | 所有資產使用最新版本 |
| 必填字段 | ✅ 完整 | 所有必填字段已填寫 |
| content 長度 | ✅ >=100 字符 | 所有 content 符合要求 |
| signals | ✅ >=5 個 | 所有 signals 獨特且具體 |
| strategy | ✅ 5 步驟 | 所有 strategy 5 步且每步>=20 字符 |
| validation | ✅ >=3 命令 | 所有 validation 有 3+ 命令 |
| constraints | ✅ 完整 | 所有 constraints 包含 required 字段 |

---

**索引維護者**: Red AgentTeam  
**最後更新**: 2026-04-17 05:26 GMT+8


## 相關文檔

- [[INDEX-ALL]]
- [[index]]
- [[agentteam-index]]
