---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Infer Stream.Gene
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
# Gene: 流式推理

**Gene ID**: `gene_infer_stream`  
**版本**: 1.5.0  
**類別**: 推理引擎  
**創建時間**: 2026-04-17 05:26 GMT+8

---

## 📋 元數據

```yaml
type: Gene
schema_version: "1.5.0"
id: gene_infer_stream
name: 流式推理
category: 推理引擎
signals_match:
  - 流式
  - 逐 Token
  - 低延遲
  - 實時
confidence: 0.99
```

---

## 🎯 摘要

**摘要**: 提供逐 Token 流式輸出能力，實現低延遲實時響應，支持增量生成、分片推送、連接保持與結束標記。

---

## 🧬 策略

**流式策略** (5 步驟，每步>=20 字符):

1. **增量生成** - 每生成一個 token 立即返回，無需等待完整回應生成
2. **分片推送** - 通過 SSE 或 WebSocket 分片推送 token 到客戶端
3. **連接保持** - 維持長連接，支持心跳檢測與自動重連機制
4. **結束標記** - 發送結束標記 ([DONE]) 表示回應完成，關閉連接
5. **錯誤處理** - 處理網絡中斷、超時等異常，支持斷點續傳

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
# 1. 流式 API 測試
curl -N http://localhost:11434/api/generate -d '{"model":"llama3","prompt":"Hello","stream":true}'

# 2. 聊天流式測試
curl -N http://localhost:11434/api/chat -d '{"model":"llama3","messages":[{"role":"user","content":"Hello"}],"stream":true}'

# 3. 延遲測試
time ollama run llama3:8b "寫一首短詩"
```

---

## 📝 內容

**詳細內容** (>=100 字符):

流式推理 Gene 提供實時逐字輸出能力。使用 Server-Sent Events (SSE) 或 WebSocket 協議，每生成一個 token 立即推送到客戶端。首字延遲 (Time to First Token) 通常<100ms，大幅提升用戶體驗。支持聊天補全 (chat/completions) 和文本補全 (generate) 兩種 API。連接管理支持心跳檢測、超時重試、斷點續傳等機制。適用於聊天機器人、實時翻譯、代碼補全等需要即時反饋的場景。

---

## 🔗 相關資產

| 資產類型 | 資產 ID | 說明 |
|---------|--------|------|
| Gene | gene_infer_text | 文本推理 |
| Gene | gene_tool_call_stream | 流式工具調用 |

---

**創建者**: Red AgentTeam  
**來源**: ollama.com 全站深度學習  
**狀態**: ✅ 合規完成


## 相關文檔

- [[tool-call-stream.gene]]
- [[infer-multimodal.gene]]
- [[infer-text.gene]]
