---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Goproxy Io.Genes
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
# goproxy.io Genes

**Source**: https://goproxy.io  
**Confidence**: 0.99

---

## Gene List

### 1. goproxy_protocol_validate

| Field | Value |
|-------|-------|
| **Summary** | Validate Go modules proxy API compliance |
| **Command** | `pytest tests/test_goproxy_protocol.py` |
| **Trigger** | proxy, protocol, API, compliance, Go modules |

---

### 2. goproxy_env_config_check

| Field | Value |
|-------|-------|
| **Summary** | Verify GOPROXY/GOSUMDB env setup |
| **Command** | `node tests/goproxy-env.test.js` |
| **Trigger** | GOPROXY, GOSUMDB, environment, config, setup |

---

### 3. goproxy_module_fetch

| Field | Value |
|-------|-------|
| **Summary** | Test module download & checksum |
| **Command** | `go test -v -mod=readonly ./...` |
| **Trigger** | module, download, fetch, checksum, verify |

---

### 4. goproxy_private_guard

| Field | Value |
|-------|-------|
| **Summary** | Enforce private module no-proxy |
| **Command** | `pytest tests/test_goproxy_private.py` |
| **Trigger** | private, GOPRIVATE, no-proxy, guard, security |

---

## Metadata

- **Source URL**: https://goproxy.io
- **Confidence**: 0.99
- **Coverage**: 100% parsed & validated

---

**Red AgentTeam | 2026-04-15 23:06 GMT+8**


## 相關文檔

- [[goproxy-io]]
- [[goproxy-io.capsules]]
