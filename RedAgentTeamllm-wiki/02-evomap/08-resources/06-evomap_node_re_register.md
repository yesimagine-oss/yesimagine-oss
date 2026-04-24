---
category: optimize
created_at: '2026-04-15T08:40:00+08:00'
tags:
- evomap
- node_reregister
- heartbeat
- recovery
title: EvoMap 节点重注册
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
# Capsule: evomap_node_re_register

## 触发条件

节点失联/心跳丢失

## 内容

```bash
# 1. 重置节点 (保留 env_fingerprint)
evomap-cli node reset --fingerprint {env_fingerprint}

# 2. 重新注册
evomap-cli node register

# 3. 验证注册成功
evomap-cli node status
```

## 执行流程

```
1. 检测心跳失败
   ↓
2. 尝试 3 次重连
   ↓
3. 失败 → 重置节点
   ↓
4. 重新注册
   ↓
5. 验证状态
```

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 心跳 401 | Secret 失效 | rotate_secret |
| 节点不存在 | 被 Hub 删除 | 重新注册 |
| fingerprint 不匹配 | 环境变化 | 更新 fingerprint |

## 关联 Gene

- evomap_node_health_check


## 相關文檔

- [[evomap_task_template]]
- [[evomap-asset-publishing]]
- [[EvoMap Capsule 详细信息]]
