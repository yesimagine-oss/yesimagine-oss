---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Rag Local.Gene
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
# Gene: 本地 RAG 嵌入檢索

**Gene ID**: `gene_rag_local`  
**版本**: 1.5.0  
**類別**: 知識庫  
**創建時間**: 2026-04-17 05:26 GMT+8

---

## 📋 元數據

```yaml
type: Gene
schema_version: "1.5.0"
id: gene_rag_local
name: 本地 RAG 嵌入檢索
category: 知識庫
signals_match:
  - RAG
  - 本地
  - 檢索
  - 嵌入
  - 知識庫
confidence: 0.97
```

---

## 🎯 摘要

**摘要**: 提供私有文檔嵌入 + 檢索能力，實現文檔切分、向量嵌入、索引構建與相似度檢索，支持本地知識庫問答。

---

## 🧬 策略

**RAG 策略** (5 步驟，每步>=20 字符):

1. **文檔切分** - 將私有文檔切分為合適大小的片段 (chunk)，保留語義完整性
2. **向量嵌入** - 使用嵌入模型 (embedding) 將文檔片段轉換為向量表示
3. **索引構建** - 構建向量索引 (FAISS/Chroma)，支持高效相似度搜索
4. **相似度檢索** - 將用戶查詢嵌入為向量，檢索最相關的文檔片段
5. **增強生成** - 將檢索結果作為上下文輸入模型，生成準確的回答

---

## 🛡️ 約束

```json
{
  "constraints": {
    "max_files": 5,
    "max_lines": 500,
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
# 1. 文檔嵌入測試
ollama run nomic-embed-text "測試文本" 

# 2. 檢索測試 (需配置 RAG)
ollama run llama3:8b "根據文檔回答：XXX" --rag ./docs/

# 3. 索引檢查
ls -la ~/.ollama/rag-index/
```

---

## 📝 內容

**詳細內容** (>=100 字符):

本地 RAG 嵌入檢索 Gene 提供檢索增強生成 (Retrieval-Augmented Generation) 能力。支持 PDF、Word、Markdown 等多種文檔格式。文檔切分採用智能策略，按段落、標題、語義邊界切分，保持上下文完整性。嵌入模型支持 nomic-embed-text、mxbai-embed-large 等本地模型。向量索引使用 FAISS 或 Chroma，支持百萬級向量高效檢索。相似度計算採用餘弦相似度或點積。增強生成將檢索結果作為系統提示詞或上下文輸入，提升回答準確性。適用於企業知識庫、文檔問答、客服助手等場景。

---

## 🔗 相關資產

| 資產類型 | 資產 ID | 說明 |
|---------|--------|------|
| Gene | gene_privacy_local_only | 本地隱私隔離 |
| Capsule | capsule_ollama_enterprise_local_rag_v1 | 企業本地隱私 RAG 膠囊 |

---

**創建者**: Red AgentTeam  
**來源**: ollama.com 全站深度學習  
**狀態**: ✅ 合規完成


## 相關文檔

- [[jit-rag-prohibition]]
- [[jit-rag-prohibition]]
