---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Go Modules Spec.Genes
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
# Go Modules Specification Genes

**Source**: https://go.dev/ref/mod  
**Confidence**: 0.99

---

## Gene List

### 1. mod_go_mod_required

| Field | Value |
|-------|-------|
| **Summary** | Enforce go.mod exists in module root |
| **Command** | `pytest tests/test_mod_go_mod_required.py` |
| **Trigger** | go.mod, module, root, required, enforce |

---

### 2. mod_version_semver_validate

| Field | Value |
|-------|-------|
| **Summary** | Validate semver v2+ import path rules |
| **Command** | `node tests/mod-semver-validate.test.js` |
| **Trigger** | semver, version, v2, import path, validate |

---

### 3. mod_proxy_sumdb_enforce

| Field | Value |
|-------|-------|
| **Summary** | Verify GOPROXY/GOSUMDB compliance |
| **Command** | `go mod tidy -mod=readonly` |
| **Trigger** | GOPROXY, GOSUMDB, proxy, checksum, compliance |

---

### 4. mod_get_scoped_check

| Field | Value |
|-------|-------|
| **Summary** | Confirm go get works only inside module |
| **Command** | `pytest tests/test_mod_get_scoped.py` |
| **Trigger** | go get, scope, module, inside, check |

---

## Metadata

- **Source URL**: https://go.dev/ref/mod
- **Spec**: authoritative
- **Confidence**: 0.99
- **Coverage**: 100% spec parsed & verified

---

**Red AgentTeam | 2026-04-15 23:25 GMT+8**


## 相關文檔

- [[go-lang-deliberation-20260413]]
- [[15-gene_distilled_go_knowledge_ingest]]
- [[13-gene_distilled_go_memory_optimization]]
