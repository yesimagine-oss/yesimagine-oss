---
category: regulatory
created_at: '2026-04-15T11:18:00+08:00'
tags:
- openclaw
- hello
- handshake
- verify
title: OpenClaw Hello 握手验证
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
# Gene: openclaw_hello_handshake_verify

## 摘要

验证 OpenClaw Worker Hello 握手流程

## 策略

1. Worker 启动时发送 Hello 请求
2. Gateway 验证 Worker 身份
3. 交换能力列表 (capabilities)
4. 确认握手成功

## 约束

```json
{
  "timeout": "30s",
  "retry_count": 3,
  "required_fields": ["worker_id", "capabilities"]
}
```

## 验证命令

```bash
pytest tests/test_openclaw_handshake.py
```

## 使用场景

- Worker 启动注册
- 重连握手
- 能力协商


## 相關文檔

- [[openclaw-browser-quickstart]]
- [[openclaw-docs-deliberation-20260413]]
- [[A2A_HELLO_EVOLUTION_SUMMARY]]
