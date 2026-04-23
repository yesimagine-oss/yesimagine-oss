---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Ollama Run.Gene
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
# Gene: 模型運行

**Gene ID**: `gene_ollama_run`  
**版本**: 1.5.0  
**類別**: 模型管理  
**創建時間**: 2026-04-17 05:26 GMT+8

---

## 📋 元數據

```yaml
type: Gene
schema_version: "1.5.0"
id: gene_ollama_run
name: 模型運行
category: 模型管理
signals_match:
  - Ollama
  - 運行
  - 對話
  - 推理
  - 交互
confidence: 0.99
```

---

## 🎯 摘要

**摘要**: 加載本地模型進行交互或非交互模式運行，支持對話、推理、批處理等多種場景，提供完整的推理體驗。

---

## 🧬 策略

**運行策略** (5 步驟，每步>=20 字符):

1. **加載模型** - 從本地倉庫加載指定模型到內存，檢查顯存/內存充足
2. **初始化會話** - 創建推理會話上下文，設置溫度、top_p 等參數
3. **接收輸入** - 接收用戶輸入 (命令行/API)，進行 token 編碼處理
4. **生成輸出** - 執行模型推理，逐 token 生成回應內容
5. **返回結果** - 返回推理結果，支持流式/非流式兩種輸出模式

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
# 1. 交互模式運行
ollama run llama3:8b "你好，請自我介紹"

# 2. 非交互模式 (管道)
echo "寫一首詩" | ollama run llama3:8b

# 3. API 模式
curl http://localhost:11434/api/generate -d '{"model":"llama3:8b","prompt":"Hello"}'
```

---

## 📝 內容

**詳細內容** (>=100 字符):

模型運行 Gene 提供完整的模型推理能力。支持交互模式 (命令行對話) 和非交互模式 (API/管道)。交互模式適合人工對話測試，非交互模式適合自動化集成。推理過程支持流式輸出，可实现逐字顯示效果。會話上下文管理確保多輪對話連貫性。資源監控防止內存/顯存溢出，大模型自動降級處理。

---

## 🔗 相關資產

| 資產類型 | 資產 ID | 說明 |
|---------|--------|------|
| Gene | gene_ollama_pull | 模型拉取 |
| Gene | gene_infer_text | 文本推理 |

---

**創建者**: Red AgentTeam  
**來源**: ollama.com 全站深度學習  
**狀態**: ✅ 合規完成


## 相關文檔

- [[ollama-start.gene]]
- [[ollama-pull.gene]]
- [[ollama-list.gene]]
