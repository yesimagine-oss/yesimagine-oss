---
category: optimize
created_at: '2026-04-15T09:27:00+08:00'
tags:
- gene
- distill
- auto
- success_rate
title: 基因自动蒸馏
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
# Capsule: gene_distill_auto

## 触发条件

10 任务成功率>70%

## 内容

```bash
# 蒸馏基因系列
./distill-gene --series gene_distilled \
  --input *.gene \
  --output distilled/
```

## 执行流程

```
1. 统计任务成功率
   ↓
2. 成功率>70% → 触发蒸馏
   ↓
3. 提取共同模式
   ↓
4. 生成蒸馏基因
   ↓
5. 存储到 distilled/
```

## 蒸馏标准

| 指标 | 阈值 | 说明 |
|------|------|------|
| 成功率 | >70% | 证明有效 |
| 任务数 | >=10 | 样本充足 |
| GDI | >60 | 质量合格 |

## 输出

- `distilled/gene_distilled_*.gene` - 蒸馏基因

## 关联 Gene

- 所有通过验证的 Gene


## 相關文檔

- [[15-gene_distilled_go_knowledge_ingest]]
- [[13-gene_distilled_go_memory_optimization]]
- [[17-gene_distilled_go_image_analysis]]
