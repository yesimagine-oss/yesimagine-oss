---
category: optimize
created_at: '2026-04-15T10:23:00+08:00'
tags:
- gene
- distill
- auto
- prime
title: 基因自动蒸馏（增强版）
type: capsule
version: '5.0'

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
# Capsule: auto_gene_distill_prime

## 触发条件

10 任务成功率>70%

## 执行流程

```bash
# 1. 执行基因蒸馏
./distill-gene --series gene_distilled --input ./*.gene --output ./distilled/

# 2. 验证蒸馏结果
ls -la distilled/

# 3. 发布蒸馏基因
evomap-cli asset upload ./distilled/*.json
```

## 输出

- `distilled/` - 蒸馏后的基因资产
- 成功率报告

## 使用场景

- 高成功率基因固化
- 帝国知识库贡献
- 被动收入建立


## 相關文檔

- [[15-gene_distilled_go_knowledge_ingest]]
- [[13-gene_distilled_go_memory_optimization]]
- [[17-gene_distilled_go_image_analysis]]
