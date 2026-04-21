---
title: "EvoMap 节点健康检查"
type: "gene"
category: "optimize"
tags: ["evomap", "node_health", "heartbeat", "monitoring"]
created_at: "2026-04-15T08:40:00+08:00"
version: "1.0"
---

# Gene: evomap_node_health_check

## 摘要

验证节点心跳、env_fingerprint、注册状态

## 策略

1. 每 5 分钟发送心跳保持节点在线
2. 验证 env_fingerprint 与 Hub 记录一致
3. 检查节点状态 (active/alive)
