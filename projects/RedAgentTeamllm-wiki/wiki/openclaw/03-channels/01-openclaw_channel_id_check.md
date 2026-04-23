---
category: regulatory
created_at: '2026-04-15T11:18:00+08:00'
tags:
- openclaw
- channel
- id
- verify
title: OpenClaw 渠道 ID 校验
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
# Gene: openclaw_channel_id_check

## 摘要

校验渠道 ID 合法性 (webchat 等)

## 策略

1. 检查渠道 ID 格式
2. 验证渠道是否存在
3. 检查渠道状态 (active/inactive)
4. 拒绝非法渠道 ID

## 约束

```json
{
  "valid_channels": ["webchat", "telegram", "discord", "feishu"],
  "format": "^[a-z_]+$"
}
```

## 验证命令

```bash
pytest tests/test_openclaw_channel.py
```

## 使用场景

- 消息路由前检查
- 渠道配置验证
- 安全审计


## 相關文檔

- [[openclaw-browser-quickstart]]
- [[openclaw-docs-deliberation-20260413]]
- [[01-openai-genes]]
