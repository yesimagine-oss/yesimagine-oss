---
category: tool
created_at: '2026-04-15T09:27:00+08:00'
tags:
- gepx
- knowledge_graph
- export
- imperial_go
title: 导出 Gepx 知识图谱
type: script
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
# 脚本：export_gepx_knowledge_graph.sh

## 功能

自动生成帝国知识图谱.gpx 格式

## 内容

```bash
#!/bin/bash
# 自动生成帝国知识图谱 .gepx
gep_export \
 --chain-id imperial_go_evolution \
 --source-genes evomap_go_core.genes \
 --source-capsules evomap_go_core.capsules \
 --schema schema/SCHEMA.md \
 --format gepx \
 --output evomap_go_knowledge.gepx \
 --negentropy-score \
 --canonical-hash
```

## 使用

```bash
./export_gepx_knowledge_graph.sh
```

## 输出

- `evomap_go_knowledge.gepx` - 知识图谱文件

## 包含内容

| 内容 | 数量 |
|------|------|
| Go Gene | 5 个 |
| Go Capsule | 4 个 |
| Schema | 1 个 |
| 负熵评分 | ✅ |
| Canonical Hash | ✅ |

## 知识图谱实体

- Go 并发模型
- 2GiB 内存最佳化
- SHA256 数字钢印
- Canonical JSON
- 负熵传播
- 高赏金任务 (>277)
- 技能蒸馏
- 帝国能力链


## 相關文檔

- [[knowledge-files-complete-list]]
- [[07-evomap_knowledge_merge]]
- [[15-gene_distilled_go_knowledge_ingest]]
