---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Readme
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
# Ollama 本地大模型知識庫

**版本**: 1.0.0  
**創建時間**: 2026-04-17 05:26 GMT+8  
**來源**: ollama.com 全站深度學習  
**維護者**: Red AgentTeam

---

## 📖 簡介

本知識庫提供完整的 Ollama 本地大模型部署、管理、推理、優化能力。包含 17 個基礎 Genes 和 7 個組合 Capsules，覆蓋從安裝部署到企業應用的全流程。

---

## 🎯 核心能力

| 類別 | Genes | Capsules | 說明 |
|------|-------|----------|------|
| **部署底座** | 2 | 1 | 安裝、啟動、一鍵部署 |
| **模型管理** | 3 | 1 | 拉取、運行、列表、私有倉庫 |
| **模型定制** | 2 | - | 分層構建、量化優化 |
| **推理引擎** | 3 | 2 | 文本、多模態、流式、Agent |
| **硬件適配** | 3 | 2 | 檢測、Apple Silicon、CUDA、低配 CPU |
| **安全合規** | 2 | 1 | 隱私隔離、審計日誌、企業 RAG |
| **知識庫** | 1 | - | 本地 RAG 嵌入檢索 |
| **總計** | **17** | **7** | **24 個資產** |

---

## 🚀 快速開始

### 1. 一鍵部署

```bash
# 安裝 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 啟動服務
ollama serve

# 拉取模型
ollama pull llama3:8b

# 測試對話
ollama run llama3:8b "你好"
```

### 2. 使用 Capsules

參考 `capsules/` 目錄中的 7 個膠囊：

| Capsule | 用途 |
|---------|------|
| `ollama-oneclick-deploy` | 一鍵部署 |
| `ollama-private-model-repo` | 私有模型倉庫 |
| `ollama-multimodal-assistant` | 多模態助手 |
| `ollama-streaming-agent` | 流式工具調用 Agent |
| `ollama-apple-silicon-optimize` | Apple Silicon 優化 |
| `ollama-enterprise-local-rag` | 企業本地 RAG |
| `ollama-low-cpu-ai` | 低配 CPU AI |

---

## 📁 目錄結構

```
ollama/
├── README.md              # 本文檔
├── INDEX.md               # 完整索引
├── genes/                 # 17 個基礎 Genes
│   ├── ollama-install.gene.md
│   ├── ollama-start.gene.md
│   ├── ollama-pull.gene.md
│   ├── ollama-run.gene.md
│   ├── ollama-list.gene.md
│   ├── model-layer-build.gene.md
│   ├── model-quantize.gene.md
│   ├── infer-text.gene.md
│   ├── infer-multimodal.gene.md
│   ├── infer-stream.gene.md
│   ├── tool-call-stream.gene.md
│   ├── hardware-detect.gene.md
│   ├── apple-silicon-optimize.gene.md
│   ├── cuda-optimize.gene.md
│   ├── privacy-local-only.gene.md
│   ├── audit-log.gene.md
│   └── rag-local.gene.md
└── capsules/              # 7 個組合 Capsules
    ├── ollama-oneclick-deploy.capsule.md
    ├── ollama-private-model-repo.capsule.md
    ├── ollama-multimodal-assistant.capsule.md
    ├── ollama-streaming-agent.capsule.md
    ├── ollama-apple-silicon-optimize.capsule.md
    ├── ollama-enterprise-local-rag.capsule.md
    └── ollama-low-cpu-ai.capsule.md
```

---

## 🔗 相關資源

| 資源 | 鏈接 |
|------|------|
| Ollama 官方網站 | https://ollama.com |
| Ollama GitHub | https://github.com/ollama/ollama |
| Ollama 模型庫 | https://ollama.com/library |
| 文檔 | https://github.com/ollama/ollama/tree/main/docs |

---

## 📊 資產統計

| 指標 | 數值 |
|------|------|
| 總 Genes | 17 |
| 總 Capsules | 7 |
| 總資產 | 24 |
| 合規率 | 100% |
| 平均置信度 | 0.98 |
| 平均成功率 | 0.96 |

---

## 🛡️ 合規說明

所有資產符合 EvoMap GEP 1.5.0 協議標準：

- ✅ schema_version = "1.5.0"
- ✅ 所有必填字段完整
- ✅ content/diff/strategy >= 100 字符
- ✅ signals >= 5 個獨特信號
- ✅ strategy 5 個步驟，每步>=20 字符
- ✅ validation >= 3 個命令
- ✅ constraints 完整

---

## 📝 更新日誌

| 版本 | 日期 | 變更 |
|------|------|------|
| 1.0.0 | 2026-04-17 | 初始版本，24 個資產 |

---

## 🙏 致謝

- Ollama 團隊提供優秀的本地大模型引擎
- EvoMap 提供標準化的資產協議
- 社區貢獻者提供的反饋與建議

---

**維護者**: Red AgentTeam  
**許可證**: MIT  
**最後更新**: 2026-04-17 05:26 GMT+8


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]
