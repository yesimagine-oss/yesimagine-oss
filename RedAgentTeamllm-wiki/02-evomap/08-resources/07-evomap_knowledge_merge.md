---
category: optimize
created_at: '2026-04-15T08:40:00+08:00'
tags:
- evomap
- knowledge_merge
- llm-wiki
- integration
title: EvoMap 知识合并
type: capsule
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
# Capsule: evomap_knowledge_merge

## 触发条件

新知识与 RedAgentTeamllm-wiki 合并

## 内容

```bash
# 合并 EvoMap 知识到 RedAgentTeamllm-wiki
llm-wiki merge --source evomap --strategy overwrite-duplicate

# 验证合并结果
llm-wiki lint --fix

# 生成合并报告
llm-wiki report --output merge-report.md
```

## 执行流程

```
1. 扫描新知识
   ↓
2. 检测重复内容
   ↓
3. 应用合并策略
   ↓
4. 运行 lint 检查
   ↓
5. 生成报告
```

## 合并策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| overwrite-duplicate | 覆盖重复 | 新知识更准确 |
| keep-both | 保留两者 | 内容互补 |
| manual-review | 人工审核 | 重要内容 |

## 关联 Gene

- evomap_asset_structure_validate


## 相關文檔

- [[evomap_task_template]]
- [[knowledge-files-complete-list]]
- [[evomap-asset-publishing]]
