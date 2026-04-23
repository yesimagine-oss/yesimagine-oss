---
category: optimize
created_at: '2026-04-15T09:35:00+08:00'
tags:
- feishu
- message
- card
- parse
title: 飞书消息卡片解析
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
# Gene: feishu_message_card_parse

## 摘要

飞书消息卡片结构解析与验证

## 策略

1. 解析卡片 JSON 结构
2. 验证 required 字段
3. 支持交互元素 (按钮/表单等)
4. 渲染预览

## 约束

```json
{
  "card_version": "1.0",
  "required_fields": ["config", "elements"]
}
```

## 验证命令

```bash
pytest tests/test_feishu_card_parse.py
```

## 使用场景

- 消息卡片发送
- 卡片模板验证
- 交互元素处理


## 相關文檔

- [[feishu-evolution-20260413]]
- [[05-evomap_asset_safe_submit]]
- [[05-openclaw_gateway_forward]]
