---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Go Get Deprecation.Capsules
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
# go get Deprecation Capsules

**Source**: https://go.dev/doc/go-get-install-deprecation  
**Confidence**: 0.99

---

## Capsule List

### 1. go_get_inside_module_only

| Field | Value |
|-------|-------|
| **Trigger** | Valid usage (official allowed pattern) |
| **Code** | ```mkdir demo; cd demo; go mod init demo; go get github.com/chromedp/chromedp@latest``` |

---

### 2. go_install_for_executables

| Field | Value |
|-------|-------|
| **Trigger** | Official replacement for binaries |
| **Code** | ```go install github.com/chromedp/chromedp-proxy@latest``` |

---

### 3. error_go_get_outside_module

| Field | Value |
|-------|-------|
| **Trigger** | Official expected error |
| **Output** | ```go: go.mod file not found in current directory or any parent directory. 'go get' is no longer supported outside a module.``` |

---

## Metadata

- **Source URL**: https://go.dev/doc/go-get-install-deprecation
- **Confidence**: 0.99
- **Canonical**: true

---

**Red AgentTeam | 2026-04-15 23:37 GMT+8**


## 相關文檔

- [[go-lang-deliberation-20260413]]
- [[15-gene_distilled_go_knowledge_ingest]]
- [[13-gene_distilled_go_memory_optimization]]
