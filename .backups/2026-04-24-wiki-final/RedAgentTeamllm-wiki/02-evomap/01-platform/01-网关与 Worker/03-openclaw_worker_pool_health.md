---
category: optimize
created_at: '2026-04-15T11:18:00+08:00'
tags:
- openclaw
- worker
- pool
- health
title: OpenClaw Worker Pool 健康检查
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
# Gene: openclaw_worker_pool_health

## 摘要

Worker Pool 节点健康与注册状态检查

## 策略

1. 定期 ping Worker 端点
2. 检查注册状态 (registered)
3. 验证心跳时间 (last_heartbeat)
4. 异常时发送告警

## 约束

```json
{
  "check_interval": "30s",
  "timeout": "5s",
  "alert_threshold": 3
}
```

## 验证命令

```bash
node tests/openclaw-worker-health.test.js
```

## 使用场景

- Worker 监控
- 故障检测
- 自动告警


## 相關文檔

- [[WECHAT-DEEP-ANALYSIS-2026-03-18]]
- [[openclaw-browser-quickstart]]
- [[openclaw-docs-deliberation-20260413]]
