---
category: llm
created_at: '2026-04-15T07:05:37+08:00'
tags:
- evomap
- auto-generated
title: K8s Health Check
type: asset
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
# K8S_Healthcheck

**來源:** `raw/k8s_healthcheck.md`  
**分類:** general  
**導入時間:** 2026-04-15T05:00:01.761842  
**狀態:** ✅ 已處理

---

# K8s 健康检查分离优化
用途：避免 Pod 因启动慢被误杀重启
核心规则：
1. livenessProbe：只检查服务是否僵死，不检查业务就绪
2. readinessProbe：检查业务是否可对外提供流量
3. 合理设置 initialDelaySeconds 避免启动期误判
作用：大幅减少服务波动、雪崩、重启风暴


## 相關文檔

- [[k8s_resource_limit]]
- [[asset02_k8s_healthcheck]]
- [[asset06_k8s_resource_limit]]
