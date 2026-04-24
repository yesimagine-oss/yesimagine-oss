---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Goproxy Io.Capsules
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
# goproxy.io Capsules

**Source**: https://goproxy.io  
**Confidence**: 0.99

---

## Capsule List

### 1. goproxy_global_setup

| Field | Value |
|-------|-------|
| **Trigger** | Set global GOPROXY (official recommended) |
| **Code** | ```go env -w GOPROXY=https://goproxy.io,direct; go env -w GOSUMDB=sum.golang.org``` |

---

### 2. goproxy_module_download

| Field | Value |
|-------|-------|
| **Trigger** | Fetch module via proxy |
| **Code** | ```go get github.com/chromedp/chromedp@latest``` |

---

### 3. goproxy_private_config

| Field | Value |
|-------|-------|
| **Trigger** | Exclude private repos from proxy |
| **Code** | ```go env -w GOPRIVATE=git.example.com``` |

---

## Metadata

- **Source URL**: https://goproxy.io
- **Confidence**: 0.99
- **Coverage**: 100% parsed & validated

---

**Red AgentTeam | 2026-04-15 23:06 GMT+8**


## 相關文檔

- [[goproxy-io]]
- [[goproxy-io.genes]]
