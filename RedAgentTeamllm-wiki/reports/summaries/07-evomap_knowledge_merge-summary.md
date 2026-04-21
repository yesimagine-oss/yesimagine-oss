---
title: "EvoMap 知识合并"
type: "capsule"
category: "optimize"
tags: ["evomap", "knowledge_merge", "llm-wiki", "integration"]
created_at: "2026-04-15T08:40:00+08:00"
version: "1.0"
---

# Capsule: evomap_knowledge_merge

## 触发条件

新知识与 RedAgentTeamllm-wiki 合并

## 内容

```bash
# 合并 EvoMap 知识到 RedAgentTeamllm-wiki
llm-wiki merge --source evomap --strategy overwrite-duplicate
