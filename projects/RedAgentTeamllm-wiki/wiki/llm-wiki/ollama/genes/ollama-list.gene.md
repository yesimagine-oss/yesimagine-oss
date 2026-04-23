---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Ollama List.Gene
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
# Gene: 本地模型列表

**Gene ID**: `gene_ollama_list`  
**版本**: 1.5.0  
**類別**: 模型管理  
**創建時間**: 2026-04-17 05:26 GMT+8

---

## 📋 元數據

```yaml
type: Gene
schema_version: "1.5.0"
id: gene_ollama_list
name: 本地模型列表
category: 模型管理
signals_match:
  - Ollama
  - 列表
  - 模型
  - 本地
  - 查詢
confidence: 0.98
```

---

## 🎯 摘要

**摘要**: 掃描本地模型倉庫，讀取元數據，結構化輸出已安裝模型清單，支持按名稱/大小/日期篩選排序。

---

## 🧬 策略

**列表策略** (5 步驟，每步>=20 字符):

1. **掃描目錄** - 掃描 ~/.ollama/models 目錄獲取所有模型文件
2. **讀取元數據** - 讀取每個模型的 manifest 文件獲取名稱、大小、創建時間
3. **結構化輸出** - 將模型信息格式化為表格或 JSON 結構化輸出
4. **返回清單** - 返回完整模型清單，包含名稱、大小、修改時間等信息
5. **可選篩選** - 支持按名稱匹配、大小範圍、時間範圍等條件篩選

---

## 🛡️ 約束

```json
{
  "constraints": {
    "max_files": 2,
    "max_lines": 200,
    "forbidden_paths": [
      "node_modules/",
      ".env",
      ".git/"
    ],
    "risk_level": "low"
  }
}
```

---

## ✅ 驗證

**驗證命令** (>=3 個):

```bash
# 1. 列出所有模型
ollama list

# 2. JSON 格式輸出
ollama list --json

# 3. 檢查模型目錄
ls -lh ~/.ollama/models/
```

---

## 📝 內容

**詳細內容** (>=100 字符):

本地模型列表 Gene 提供查詢已安裝模型的能力。掃描 ~/.ollama/models 目錄，解析每个模型的 manifest 文件，提取名稱、版本、大小、創建時間等元數據。輸出支持表格格式 (人類可讀) 和 JSON 格式 (機器可讀)。支持按名稱模糊匹配篩選，方便查找特定模型。列表信息包括模型名稱、標籤、大小、修改時間、Digest 哈希值等完整信息。

---

## 🔗 相關資產

| 資產類型 | 資產 ID | 說明 |
|---------|--------|------|
| Gene | gene_ollama_pull | 模型拉取 |
| Capsule | capsule_ollama_private_model_repo_v1 | 私有模型倉庫膠囊 |

---

**創建者**: Red AgentTeam  
**來源**: ollama.com 全站深度學習  
**狀態**: ✅ 合規完成


## 相關文檔

- [[ollama-run.gene]]
- [[ollama-start.gene]]
- [[ollama-pull.gene]]
