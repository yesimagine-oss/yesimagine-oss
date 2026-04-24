---
category: regulatory
created_at: '2026-04-15T11:18:00+08:00'
tags:
- openclaw
- config
- schema
- verify
title: OpenClaw 配置文件校验
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
# Gene: openclaw_config_schema_verify

## 摘要

OpenClaw 配置文件结构校验

## 策略

1. 加载配置文件 (openclaw.json)
2. 验证 JSON5 语法
3. 检查 required 字段
4. 验证字段类型和格式

## 约束

```json
{
  "required_fields": ["gateway", "workers", "channels"],
  "format": "json5"
}
```

## 验证命令

```bash
node tests/openclaw-config-schema.test.js
```

## 使用场景

- 启动前配置检查
- 配置更新验证
- 错误预防


## 相關文檔

- [[serper-api-config]]
- [[WECHAT-DEEP-ANALYSIS-2026-03-18]]
- [[openclaw-browser-quickstart]]
