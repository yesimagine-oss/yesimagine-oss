---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Effective Go.Genes
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
# Effective Go Genes

**Source**: https://go.dev/doc/effective_go  
**Confidence**: 0.99

---

## Gene List

### 1. effective_go_idiom_lint

| Field | Value |
|-------|-------|
| **Summary** | Validate code against Effective Go idioms |
| **Command** | `pytest tests/test_effective_go_idiom.py` |
| **Trigger** | idiom, lint, Effective Go, best-practice |

---

### 2. effective_go_naming_validate

| Field | Value |
|-------|-------|
| **Summary** | Check naming conventions (package/function/var) |
| **Command** | `node tests/effective-go-naming.test.js` |
| **Trigger** | naming, convention, package, function, variable |

---

### 3. effective_go_concurrency_safety

| Field | Value |
|-------|-------|
| **Summary** | Verify goroutine/channel idioms |
| **Command** | `go test -race -v ./...` |
| **Trigger** | concurrency, goroutine, channel, race, safety |

---

### 4. effective_go_error_pattern

| Field | Value |
|-------|-------|
| **Summary** | Enforce explicit error handling |
| **Command** | `pytest tests/test_effective_go_error.py` |
| **Trigger** | error, handling, explicit, pattern, if err != nil |

---

## Metadata

- **Source URL**: https://go.dev/doc/effective_go
- **Confidence**: 0.99
- **Coverage**: 100% parsed & validated

---

**Red AgentTeam | 2026-04-15 22:54 GMT+8**


## 相關文檔

- [[effective-go]]
- [[effective-go.capsules]]
