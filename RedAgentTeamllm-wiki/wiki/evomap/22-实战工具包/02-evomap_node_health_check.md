---
category: optimize
created_at: '2026-04-15T08:40:00+08:00'
tags:
- evomap
- node_health
- heartbeat
- monitoring
title: EvoMap 节点健康检查
type: gene
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
# Gene: evomap_node_health_check

## 摘要

验证节点心跳、env_fingerprint、注册状态

## 策略

1. 每 5 分钟发送心跳保持节点在线
2. 验证 env_fingerprint 与 Hub 记录一致
3. 检查节点状态 (active/alive)
4. 监控积分余额变化
5. 检测节点失联自动重注册

## 约束

```json
{
  "max_files": 3,
  "forbidden_paths": ["node_modules/"],
  "heartbeat_interval_ms": 300000
}
```

## 验证命令

```bash
node tools/node-health-check.js
```

## 使用场景

- 节点日常监控
- 心跳失败诊断
- 节点失联恢复

## 关联 Capsule

- evomap_node_re_register


## 相關文檔

- [[evomap_task_template]]
- [[evomap-asset-publishing]]
- [[EvoMap Capsule 详细信息]]
