---
category: llm
created_at: '2026-04-20'
tags:
- llm
- auto-generated
title: Service Storm Protect
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
# 服务重启风暴防护
问题：服务崩溃 → 快速重启 → 资源耗尽 → 更多服务崩溃
防护策略：
1. 指数退避重启策略（Exponential Backoff）
2. 设置最大重启次数限制
3. 依赖健康检查，避免崩溃服务快速重建
目标：保证节点稳定，防止级联故障


## 相關文檔

- [[asset04_service_storm_protect]]
- [[04-a2a_validate_dryrun_protect]]
- [[asset04_service_storm_protect]]
