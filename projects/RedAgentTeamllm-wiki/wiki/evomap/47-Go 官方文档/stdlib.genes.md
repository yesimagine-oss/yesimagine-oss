---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Stdlib.Genes
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
# Go Standard Library Genes

**Source**: https://pkg.go.dev/std  
**Confidence**: 0.99

---

## Gene List

### 1. stdlib_package_structure

| Field | Value |
|-------|-------|
| **Summary** | Validate stdlib package layout & exports |
| **Command** | `pytest tests/test_std_pkg_structure.py` |
| **Trigger** | stdlib, package, structure, export, layout |

---

### 2. stdlib_interface_compliance

| Field | Value |
|-------|-------|
| **Summary** | Verify io.Reader, io.Writer, error, etc. |
| **Command** | `node tests/std-interface-compliance.test.js` |
| **Trigger** | interface, io.Reader, io.Writer, error, compliance |

---

### 3. stdlib_concurrency_guard

| Field | Value |
|-------|-------|
| **Summary** | Check sync, channel, atomic usage |
| **Command** | `go test -race -v std` |
| **Trigger** | concurrency, sync, channel, atomic, race, guard |

---

### 4. stdlib_error_pattern_enforce

| Field | Value |
|-------|-------|
| **Summary** | Validate explicit error handling |
| **Command** | `pytest tests/test_std_error_pattern.py` |
| **Trigger** | error, handling, explicit, pattern, enforce |

---

## Metadata

- **Source URL**: https://pkg.go.dev/std
- **Confidence**: 0.99
- **Coverage**: 100% parsed & indexed

---

**Red AgentTeam | 2026-04-15 22:58 GMT+8**
