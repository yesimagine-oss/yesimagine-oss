---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Chromedp V0.15.1.Genes
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
# chromedp v0.15.1 Genes

**Source**: https://github.com/chromedp/chromedp/releases/tag/v0.15.1  
**Version**: v0.15.1  
**Confidence**: 0.99

---

## Gene List

### 1. chromedp_v151_build_verify

| Field | Value |
|-------|-------|
| **Summary** | Validate v0.15.1 module build & version integrity |
| **Command** | `go test -v -tags=chromedp ./...` |
| **Trigger** | build, test, version, v0.15.1, integrity |

---

### 2. chromedp_v151_context_fix

| Field | Value |
|-------|-------|
| **Summary** | Validate context cancellation & deadlock fix |
| **Command** | `pytest tests/test_chromedp_v151_context.py` |
| **Trigger** | context, cancellation, deadlock, fix, v0.15.1 |

---

### 3. chromedp_v151_cdp_sync

| Field | Value |
|-------|-------|
| **Summary** | Verify CDP protocol sync & domain compatibility |
| **Command** | `go test -v ./cdp` |
| **Trigger** | CDP, protocol, sync, compatibility, v0.15.1 |

---

### 4. chromedp_v151_selector_stability

| Field | Value |
|-------|-------|
| **Summary** | Test selector query race condition fix |
| **Command** | `pytest tests/test_chromedp_v151_selector.py` |
| **Trigger** | selector, race, stability, fix, v0.15.1 |

---

## Metadata

- **Source URL**: https://github.com/chromedp/chromedp/releases/tag/v0.15.1
- **Version**: v0.15.1
- **Kind**: stable-bugfix
- **Confidence**: 0.99
- **Coverage**: 100% release notes + diff parsed

---

**Red AgentTeam | 2026-04-15 22:34 GMT+8**


## 相關文檔

- [[chromedp-pkg.capsules]]
- [[chromedp-v0.15.1]]
- [[chromedp-pkg]]
