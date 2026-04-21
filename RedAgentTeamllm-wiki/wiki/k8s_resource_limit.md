---
category: llm
created_at: '2026-04-15T07:05:36+08:00'
tags:
- evomap
- auto-generated
title: K8s Resource Limit
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
# K8S_Resource_Limit

**來源:** `raw/k8s_resource_limit.md`  
**分類:** general  
**導入時間:** 2026-04-15T05:00:01.755891  
**狀態:** ✅ 已處理

---

# K8s 资源限制与请求配置
核心配置：
1. requests：调度依据，保证最低可用资源
2. limits：硬上限，防止服务耗尽节点资源
配置原则：
- 不设 limits 容易导致节点 OOM
- requests 过大会导致调度困难
- 结合监控设置合理区间
适用：低配置服务器（如 2C2G 青岛节点）


## 相關文檔

- [[k8s_healthcheck]]
- [[asset02_k8s_healthcheck]]
- [[asset06_k8s_resource_limit]]
