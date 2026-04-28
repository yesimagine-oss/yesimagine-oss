---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Go Get Deprecation.Genes
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
# go get Deprecation Genes

**Source**: https://go.dev/doc/go-get-install-deprecation  
**Confidence**: 0.99

---

## Gene List

### 1. go_get_outside_module_error

| Field | Value |
|-------|-------|
| **Summary** | Validate hard error when go get outside module |
| **Command** | `pytest tests/test_go_get_outside_mod.py` |
| **Trigger** | go get, outside, module, error, deprecation |

---

### 2. go_get_only_modifies_modules

| Field | Value |
|-------|-------|
| **Summary** | Verify go get only edits go.mod (no install) |
| **Command** | `node tests/go-get-mod-only.test.js` |
| **Trigger** | go get, modifies, go.mod, dependencies, edit |

---

### 3. go_install_for_binaries

| Field | Value |
|-------|-------|
| **Summary** | Enforce go install @latest for executables |
| **Command** | `go install golang.org/x/tools/cmd/gopls@latest` |
| **Trigger** | go install, executables, binaries, @latest |

---

### 4. go_version_1_18_enforcement

| Field | Value |
|-------|-------|
| **Summary** | Validate strict behavior >= Go 1.18 |
| **Command** | `go version && go get github.com/chromedp/chromedp` |
| **Trigger** | Go 1.18, version, enforcement, strict |

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
