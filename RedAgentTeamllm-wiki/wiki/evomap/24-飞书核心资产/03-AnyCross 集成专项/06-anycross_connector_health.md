---
category: optimize
created_at: '2026-04-15T11:08:00+08:00'
tags:
- anycross
- connector
- health
- check
title: AnyCross 连接器健康检查
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
# Gene: anycross_connector_health

## 摘要

连接器可用性与健康检查

## 策略

1. 定期 ping 连接器端点
2. 检查响应时间和状态码
3. 验证认证凭证有效性
4. 异常时发送告警

## 约束

```json
{
  "check_interval": "60s",
  "timeout": "5s",
  "alert_threshold": 3
}
```

## 验证命令

```bash
node tests/anycross-connector-health.test.js
```

## 使用场景

- 连接器监控
- 故障检测
- 自动告警


## 相關文檔

- [[06-evomap_node_re_register]]
- [[02-evomap_node_health_check]]
- [[03-openclaw_worker_pool_health]]
