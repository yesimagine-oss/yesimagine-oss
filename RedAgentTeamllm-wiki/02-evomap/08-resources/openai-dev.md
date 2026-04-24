---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Openai Dev
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
# OpenAI 开发者 API - 官方文档

**来源:** developers.openai.com (118 页完整覆盖)
**置信度:** 0.99
**入库日期:** 2026-04-15

---

## 核心功能

| 功能 | 说明 |
|------|------|
| Chat | GPT-4/GPT-3.5 对话 |
| Embedding | 文本向量化 |
| 流式处理 | SSE 实时输出 |
| 限流重试 | 指数退避 |

---

## 项目应用

| 项目 | 用途 | 节省 |
|------|------|------|
| go-image-skill | 图像问答/描述 | ~3h |
| 无头浏览器 | 内容摘要/智能填充 | ~3h |
| **总计** | - | **~6h** |

---

## 与 Gemini 选择建议

| 场景 | 推荐 |
|------|------|
| 多模态 | Gemini |
| 纯文本 | OpenAI |
| Embedding | OpenAI |
| 中文 | Gemini |

---

**结论:** 官方开发者文档，更完整，建议入库

---

Red AgentTeam｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...

## 相關文檔

- [[01-openai-genes]]
- [[02-openai-capsules]]
- [[OpenAI 集成学习记录]]
