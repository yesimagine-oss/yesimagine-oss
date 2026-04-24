---
category: optimize
created_at: '2026-04-15T09:27:00+08:00'
tags:
- go
- negentropy
- solidify
- knowledge
title: Go 负熵固化
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
# Capsule: go_negentropy_solidify

## 触发条件

新知识区块完成解析

## 内容

```bash
# 创建目录结构
mkdir -p raw/ wiki/ schema/

# 复制源代码
cp source.go raw/

# 生成文档
go doc ./ > wiki/go-concurrency.md

# 更新 schema
echo "updated: $(date)" >> schema/SCHEMA.md
```

## 执行流程

```
1. 解析 Go 源代码
   ↓
2. 提取文档注释
   ↓
3. 生成 wiki 文档
   ↓
4. 更新 schema
```

## 输出

- `raw/source.go` - 原始代码
- `wiki/go-concurrency.md` - 文档
- `schema/SCHEMA.md` - Schema 更新

## 关联 Gene

- go_concurrency_high_negentropy


## 相關文檔

- [[go-lang-deliberation-20260413]]
- [[06-evomap_node_re_register]]
- [[15-gene_distilled_go_knowledge_ingest]]
