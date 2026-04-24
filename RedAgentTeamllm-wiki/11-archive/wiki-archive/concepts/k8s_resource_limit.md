---
category: concept
created_at: '2026-04-14'
tags:
- concept
- auto-generated
title: K8S Resource Limit
type: concept
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
# K8s 资源限制与请求配置

**類型:** general
**來源:** llm-wiki
**標籤:** 
**導入時間:** 2026-04-13T01:23:13.666Z

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


---

**結構化元數據:**
- 原始文件：k8s_resource_limit.md
- 導入日期：2026-04-13T01:23:13.666Z
- 處理狀態：completed

## 參考

- [[Asset06_K8S_Resource_Limit]]


## 相關文檔

- [[k8s_healthcheck]]
- [[asset02_k8s_healthcheck]]
- [[asset06_k8s_resource_limit]]
