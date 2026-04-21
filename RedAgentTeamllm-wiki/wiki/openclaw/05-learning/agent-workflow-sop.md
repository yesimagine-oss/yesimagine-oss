---
title: "AI 代理標準工作流程 SOP"
type: "sop"
category: "agent_workflow"
tags: ["agent", "workflow", "sop", "knowledge_base"]
created_at: "2026-04-20"
version: "1.0"
provenance:
  source_url: "internal-sop"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "manual"
  trust_score: 1.0
trust_level: "human-verified"
evidence_level: "人工制定"
---

# 📋 AI 代理標準工作流程

## 流程圖

```
1. 接收指令 → 2. 查知識庫 → 3. 規劃執行 → 4. 執行操作 → 5. 知識沉澱 → 6. 反饋結果
```

## 步驟詳解

| 步驟 | 說明 | 關鍵動作 |
|------|------|----------|
| **1. 接收指令** | 理解用戶需求 | 確認目標 |
| **2. 查知識庫** | 搜索 RedAgentTeamllm-wiki | 避免重複造輪子 |
| **3. 規劃執行** | 拆解步驟 | 評估風險 |
| **4. 執行操作** | 調用工具 | 實時驗證 |
| **5. 知識沉澱** | 入庫 | 驗證報告/Gene/Capsule |
| **6. 反饋結果** | 精簡回覆 | 15-20 行 |

## 核心原則

- **先查知識庫** - 避免重複工作
- **重要操作先確認** - 降低風險
- **知識必入庫** - 知識複利增長
- **精簡回覆** - 省 token

## 相關資產

- `genes/gene_agent_workflow_sop.json`
- `capsules/capsule_agent_workflow_check.json`
