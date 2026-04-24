---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: 02 Openai Capsules
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
# OpenAI Capsules

**来源:** OpenAI Open Models (42 页完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

| # | Capsule | 用途 |
|---|---------|------|
| 1 | `openai_list_open_models` | 获取可用模型列表 |
| 2 | `openai_model_chat_call` | Chat API 调用 |
| 3 | `openai_model_validate` | 模型存在性检查 |

---

## go-image-skill 集成

```go
// 获取模型列表
GET https://api.openai.com/v1/models

// 调用 Chat
POST /v1/chat/completions
{"model":"gpt-4o","messages":[...]}

// 验证模型
model, _ := client.GetModel(ctx, "gpt-4o")
```

**节省:** ~3h


## 相關文檔

- [[01-openai-genes]]
- [[openai-dev]]
- [[02-evomap_node_health_check]]
