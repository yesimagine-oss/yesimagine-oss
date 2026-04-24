---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Tool Call Stream.Gene
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
# Gene: 流式工具調用

**Gene ID**: `gene_tool_call_stream`  
**版本**: 1.5.0  
**類別**: Agent 能力  
**創建時間**: 2026-04-17 05:26 GMT+8

---

## 📋 元數據

```yaml
type: Gene
schema_version: "1.5.0"
id: gene_tool_call_stream
name: 流式工具調用
category: Agent 能力
signals_match:
  - 工具調用
  - 流式
  - Agent
  - 執行
  - 增量
confidence: 0.97
```

---

## 🎯 摘要

**摘要**: 支持邊輸出邊執行工具調用，實現增量解析、工具匹配、並行執行與結果回填，提升 Agent 自動化效率。

---

## 🧬 策略

**調用策略** (5 步驟，每步>=20 字符):

1. **增量解析** - 流式解析模型輸出，實時檢測工具調用意圖與參數
2. **工具匹配** - 根據意圖匹配可用工具 (搜索/計算/API)，驗證參數格式
3. **並行執行** - 並行執行多個工具調用，超時控制與錯誤隔離處理
4. **結果回填** - 將工具執行結果回填到對話上下文，繼續生成回應
5. **流式輸出** - 將最終結果流式輸出到客戶端，保持實時響應體驗

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
    "risk_level": "medium"
  }
}
```

---

## ✅ 驗證

**驗證命令** (>=3 個):

```bash
# 1. 工具調用測試 (需配置工具)
ollama run llama3:8b "查詢今天的天氣" --tools weather

# 2. API 測試
curl http://localhost:11434/api/generate -d '{"model":"llama3","prompt":"搜索 OpenClaw","tools":[{"name":"search"}]}'

# 3. 執行日誌檢查
tail -f ~/.ollama/logs/tool-calls.log
```

---

## 📝 內容

**詳細內容** (>=100 字符):

流式工具調用 Gene 提供 Agent 自動化執行能力。支持搜索、計算、API 調用、文件操作等多種工具類型。增量解析機制在模型生成過程中實時檢測工具調用意圖，無需等待完整輸出。並行執行支持多個工具同時執行，提升效率。結果回填將工具執行結果無縫整合到對話中，保持上下文連貫。適用於智能助手、自動化工作流、RAG 檢索增強等場景。

---

## 🔗 相關資產

| 資產類型 | 資產 ID | 說明 |
|---------|--------|------|
| Gene | gene_infer_stream | 流式推理 |
| Capsule | capsule_ollama_streaming_agent_v1 | 流式工具調用 Agent 膠囊 |

---

**創建者**: Red AgentTeam  
**來源**: ollama.com 全站深度學習  
**狀態**: ✅ 合規完成


## 相關文檔

- [[infer-stream.gene]]
