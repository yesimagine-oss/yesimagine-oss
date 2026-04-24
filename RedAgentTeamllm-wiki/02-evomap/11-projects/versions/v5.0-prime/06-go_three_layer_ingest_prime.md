---
category: optimize
created_at: '2026-04-15T10:23:00+08:00'
tags:
- go
- wiki
- ingest
- three_layer
- prime
title: Go 三层摄入流程（增强版）
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
# Capsule: go_three_layer_ingest_prime

## 触发条件

新知识区块解析完成

## 执行流程

```bash
# 1. 创建三层目录结构
mkdir -p raw/ wiki/ schema/

# 2. 复制源代码到 raw 层
cp source.go raw/

# 3. 生成文档到 wiki 层
go doc ./ > wiki/go-concurrency-prime.md

# 4. 记录 Schema 版本
echo "go_prime_convention_2026" >> schema/SCHEMA.md
```

## 输出

- `raw/` - 原始源代码
- `wiki/` - 生成的文档
- `schema/` - Schema 版本记录

## 使用场景

- Go 知识库建设
- 自动文档生成
- 知识版本管理


## 相關文檔

- [[docker_layer_cache]]
- [[asset01_docker_layer_cache]]
- [[go-lang-deliberation-20260413]]
