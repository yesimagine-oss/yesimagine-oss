---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Gemini
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
# Gemini API - 多模态 AI

**来源:** Google AI (96 页完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## 核心功能

| 功能 | 说明 |
|------|------|
| Chat | 多轮对话 |
| Vision | 图像理解 (原生) |
| 流式处理 | SSE 实时输出 |
| 函数调用 | 工具集成 |

---

## 项目应用

| 项目 | 用途 | 节省 |
|------|------|------|
| go-image-skill | 图像问答/描述 | ~5h |
| 无头浏览器 | 截图分析/页面总结 | ~3h |
| **总计** | - | **~8h** |

---

## 代码示例

```go
// 图像 + 文本查询
{
  "contents": [{
    "parts": [
      {"text": "describe"},
      {"inline_data": {
        "mime_type": "image/jpeg",
        "data": "base64..."
      }}
    ]
  }]
}
```

---

## 与 OpenAI 选择建议

| 场景 | 推荐 |
|------|------|
| 多模态 | Gemini (原生) |
| 纯文本 | 两者均可 |
| 中文 | Gemini |
| 免费额度 | Gemini |

---

**结论:** 多模态 AI 首选，建议入库

---

Red AgentTeam｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

## 相關文檔

- [[Google Gemini 集成完全指南]]
