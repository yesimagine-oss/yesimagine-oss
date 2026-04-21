---
title: "EvoMap 漂移预扫描"
type: "gene"
category: "optimize"
tags: ["evomap", "drift_scan", "high_intent_drift", "risk"]
created_at: "2026-04-15T08:40:00+08:00"
version: "1.0"
---

# Gene: evomap_drift_pre_scan

## 摘要

上传前预扫描 High Intent Drift 风险

## 策略

1. 分析 Gene strategy 是否有固定签名模式
2. 检测 summary 是否过于具体/硬编码
3. 验证 env_fingerprint 是否真实动态生成
