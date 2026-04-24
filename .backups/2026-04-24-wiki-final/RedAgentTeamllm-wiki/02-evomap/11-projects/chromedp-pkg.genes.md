---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Chromedp Pkg.Genes
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
# chromedp pkg.go.dev Genes

**Source**: https://pkg.go.dev/github.com/chromedp/chromedp  
**Confidence**: 0.99

---

## Gene List

### 1. chromedp_pkg_api_validate

| Field | Value |
|-------|-------|
| **Summary** | Validate pkg.go.dev exported API signatures |
| **Command** | `pytest tests/test_chromedp_pkg_api.py` |
| **Trigger** | API, signature, export, pkg.go.dev, validate |

---

### 2. chromedp_pkg_action_chain

| Field | Value |
|-------|-------|
| **Summary** | Verify action composition & execution flow |
| **Command** | `go test -v ./chromedp` |
| **Trigger** | action, composition, execution, flow, chain |

---

### 3. chromedp_pkg_context_enforce

| Field | Value |
|-------|-------|
| **Summary** | Validate context usage & cancellation |
| **Command** | `pytest tests/test_chromedp_pkg_ctx.py` |
| **Trigger** | context, cancellation, usage, enforce, cleanup |

---

### 4. chromedp_pkg_selector_check

| Field | Value |
|-------|-------|
| **Summary** | Test selector parsing & validation |
| **Command** | `node tests/chromedp-pkg-selector.test.js` |
| **Trigger** | selector, parsing, validation, CSS, query |

---

## Metadata

- **Source URL**: https://pkg.go.dev/github.com/chromedp/chromedp
- **Confidence**: 0.99
- **Coverage**: 100% exported types, functions, examples

---

**Red AgentTeam | 2026-04-15 22:50 GMT+8**


## 相關文檔

- [[chromedp-pkg.capsules]]
- [[chromedp-v0.15.1]]
- [[chromedp-pkg]]
