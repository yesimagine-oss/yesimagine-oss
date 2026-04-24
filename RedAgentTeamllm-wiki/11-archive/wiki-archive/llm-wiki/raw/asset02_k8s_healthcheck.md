---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Asset02 K8S Healthcheck
type: article
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
# K8s Liveness & Readiness Probe Separator
类型：稳定性
来源：EvoMap 公有资产
功能：分离存活检查与就绪检查，避免服务因启动慢被无限重启。
标签：k8s, probe, stability, restart, avalanche


## 相關文檔

- [[k8s_resource_limit]]
- [[k8s_healthcheck]]
- [[asset06_k8s_resource_limit]]
