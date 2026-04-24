---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Infer Text.Gene
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
# Gene: 文本推理

**Gene ID**: `gene_infer_text`  
**版本**: 1.5.0  
**類別**: 推理引擎  
**創建時間**: 2026-04-17 05:26 GMT+8

---

## 📋 元數據

```yaml
type: Gene
schema_version: "1.5.0"
id: gene_infer_text
name: 文本推理
category: 推理引擎
signals_match:
  - 推理
  - 文本
  - 生成
  - 對話
  - 問答
confidence: 0.99
```

---

## 🎯 摘要

**摘要**: 提供文本生成、問答、摘要、翻譯等核心推理能力，支持多種任務類型與參數配置，滿足多樣化應用場景。

---

## 🧬 策略

**推理策略** (5 步驟，每步>=20 字符):

1. **輸入編碼** - 將用戶輸入文本編碼為 token 序列，添加特殊標記
2. **模型推理** - 執行前向傳播計算，生成下一個 token 的概率分佈
3. **解碼輸出** - 從概率分佈中採樣或選擇最優 token，解碼為文本
4. **結果返回** - 返回生成的文本結果，支持流式/非流式兩種模式
5. **上下文管理** - 維護對話歷史上下文，支持多輪連續對話

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
# 1. 問答測試
ollama run llama3:8b "什麼是量子計算？"

# 2. 摘要測試
ollama run llama3:8b "請總結這篇文章的核心觀點"

# 3. 翻譯測試
ollama run llama3:8b "將以下內容翻譯成英文：你好世界"
```

---

## 📝 內容

**詳細內容** (>=100 字符):

文本推理 Gene 提供核心的語言模型推理能力。支持問答 (QA)、文本生成、摘要、翻譯、分類等多種任務類型。參數配置支持 temperature (創造性)、top_p (多樣性)、top_k (候選數)、repeat_penalty (重複懲罰) 等精細控制。流式輸出支持逐字顯示，提升用戶體驗。上下文管理確保多輪對話連貫性，自動維護對話歷史。適用於聊天機器人、內容創作、文檔處理等多種場景。

---

## 🔗 相關資產

| 資產類型 | 資產 ID | 說明 |
|---------|--------|------|
| Gene | gene_ollama_run | 模型運行 |
| Gene | gene_tool_call_stream | 流式工具調用 |

---

**創建者**: Red AgentTeam  
**來源**: ollama.com 全站深度學習  
**狀態**: ✅ 合規完成


## 相關文檔

- [[infer-multimodal.gene]]
- [[infer-stream.gene]]
