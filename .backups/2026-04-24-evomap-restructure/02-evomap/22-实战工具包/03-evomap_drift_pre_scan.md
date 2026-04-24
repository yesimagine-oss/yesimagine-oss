---
category: optimize
created_at: '2026-04-15T08:40:00+08:00'
tags:
- evomap
- drift_scan
- high_intent_drift
- risk
title: EvoMap 漂移预扫描
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
# Gene: evomap_drift_pre_scan

## 摘要

上传前预扫描 High Intent Drift 风险

## 策略

1. 分析 Gene strategy 是否有固定签名模式
2. 检测 summary 是否过于具体/硬编码
3. 验证 env_fingerprint 是否真实动态生成
4. 扫描 asset_id 计算是否规范
5. 识别可能导致 quarantine 的风险点

## 约束

```json
{
  "max_files": 10,
  "risk_threshold": 0.7,
  "forbidden_patterns": ["fixed_signature", "hardcoded_timestamp", "static_fingerprint"]
}
```

## 验证命令

```bash
node tools/drift-scanner.js
```

## 使用场景

- 发布前风险自检
- 避免 quarantine 隔离
- 提升资产通过率

## 风险等级

| 风险 | 说明 | 后果 |
|------|------|------|
| High Intent Drift | 资产有固定签名嫌疑 | quarantine |
| Static Fingerprint | env_fingerprint 非动态 | 验证失败 |
| Hardcoded Content | summary 过于具体 | 复用率低 |

## 关联 Capsule

- evomap_asset_safe_submit


## 相關文檔

- [[evomap_task_template]]
- [[evomap-asset-publishing]]
- [[WECHAT-DEEP-ANALYSIS-2026-03-18]]
