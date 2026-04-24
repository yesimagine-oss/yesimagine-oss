---
title: "EvoMap 节点重注册"
type: "capsule"
category: "optimize"
tags: ["evomap", "node_reregister", "heartbeat", "recovery"]
created_at: "2026-04-15T08:40:00+08:00"
version: "1.0"
---

# Capsule: evomap_node_re_register

## 触发条件

节点失联/心跳丢失

## 内容

```bash
# 1. 重置节点 (保留 env_fingerprint)
evomap-cli node reset --fingerprint {env_fingerprint}
