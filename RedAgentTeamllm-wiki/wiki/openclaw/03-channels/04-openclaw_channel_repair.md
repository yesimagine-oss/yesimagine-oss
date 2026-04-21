---
category: optimize
created_at: '2026-04-15T11:18:00+08:00'
tags:
- openclaw
- channel
- repair
- fix
title: OpenClaw 渠道修复
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
# Capsule: openclaw_channel_repair

## 触发条件

渠道 ID 无效 / 网关崩溃

## 执行流程

```bash
# 1. 列出渠道
openclaw-cli channel list

# 2. 修复渠道
openclaw-cli channel repair --id webchat

# 3. 重启网关
systemctl restart openclaw-gateway
```

## 输出

- 修复结果
- 渠道状态

## 使用场景

- 渠道故障恢复
- 网关重启
- 配置修复


## 相關文檔

- [[openclaw-browser-quickstart]]
- [[openclaw-docs-deliberation-20260413]]
- [[04-evomap_asset_hash_verify]]
