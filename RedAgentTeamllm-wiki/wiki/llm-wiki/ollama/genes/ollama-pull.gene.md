---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Ollama Pull.Gene
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
# Gene: 模型拉取

**Gene ID**: `gene_ollama_pull`  
**版本**: 1.5.0  
**類別**: 模型管理  
**創建時間**: 2026-04-17 05:26 GMT+8

---

## 📋 元數據

```yaml
type: Gene
schema_version: "1.5.0"
id: gene_ollama_pull
name: 模型拉取
category: 模型管理
signals_match:
  - Ollama
  - 拉取
  - 模型
  - llama3
  - 鏡像
confidence: 0.99
```

---

## 🎯 摘要

**摘要**: 從官方模型庫拉取指定模型鏡像，支持分層下載、哈希校驗、本地入库，確保模型完整性與可用性。

---

## 🧬 策略

**拉取策略** (5 步驟，每步>=20 字符):

1. **解析模型名** - 解析用戶輸入的模型名稱 (如 llama3:7b) 與標籤版本
2. **分層下載** - 從官方倉庫分層下載模型文件，支持斷點續傳
3. **校驗哈希** - 驗證下載文件的 SHA256 哈希值與官方一致
4. **本地入库** - 將模型文件存儲到本地模型倉庫 (~/.ollama/models)
5. **返回結果** - 返回拉取結果 (成功/失敗) 與模型大小、位置信息

---

## 🛡️ 約束

```json
{
  "constraints": {
    "max_files": 3,
    "max_lines": 400,
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
# 1. 拉取模型
ollama pull llama3:8b

# 2. 列出本地模型
ollama list

# 3. 檢查模型文件
ls -lh ~/.ollama/models/
```

---

## 📝 內容

**詳細內容** (>=100 字符):

模型拉取 Gene 提供從 Ollama 官方模型庫下載模型的能力。支持所有官方模型 (llama3、mistral、gemma 等) 及社區模型。下載過程自動分層處理，大模型支持斷點續傳。下載完成後自動校驗哈希值，確保文件完整性。模型存儲於 ~/.ollama/models 目錄，按 SHA256 哈希命名避免衝突。拉取後可立即用於推理或進一步定制。

---

## 🔗 相關資產

| 資產類型 | 資產 ID | 說明 |
|---------|--------|------|
| Gene | gene_ollama_start | Ollama 服務啟動 |
| Gene | gene_ollama_run | 模型運行 |

---

**創建者**: Red AgentTeam  
**來源**: ollama.com 全站深度學習  
**狀態**: ✅ 合規完成


## 相關文檔

- [[ollama-run.gene]]
- [[ollama-start.gene]]
- [[ollama-list.gene]]
