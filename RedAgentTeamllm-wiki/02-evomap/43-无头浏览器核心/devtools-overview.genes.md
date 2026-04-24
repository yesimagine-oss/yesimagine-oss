---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Devtools Overview.Genes
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
# Chrome DevTools Overview Genes

**Source**: https://developer.chrome.com/docs/devtools/overview  
**Confidence**: 0.99

---

## Gene List

### 1. devtools_panel_detect

| Field | Value |
|-------|-------|
| **Summary** | Validate DevTools panel availability & state |
| **Command** | `pytest tests/test_devtools_panels.py` |
| **Trigger** | DevTools, panel, availability, state, UI |

---

### 2. devtools_cdp_binding_verify

| Field | Value |
|-------|-------|
| **Summary** | Verify DevTools-CDP command mapping |
| **Command** | `node tests/devtools-cdp-bind.test.js` |
| **Trigger** | DevTools, CDP, binding, command, mapping |

---

### 3. devtools_remote_debug_check

| Field | Value |
|-------|-------|
| **Summary** | Validate remote debugging port & connection |
| **Command** | `pytest tests/test_devtools_remote.py` |
| **Trigger** | remote, debugging, port, connection, 9222 |

---

### 4. devtools_workflow_lint

| Field | Value |
|-------|-------|
| **Summary** | Lint official debug workflow correctness |
| **Command** | `node tests/devtools-workflow.test.js` |
| **Trigger** | workflow, debug, lint, correctness, official |

---

## Metadata

- **Source URL**: https://developer.chrome.com/docs/devtools/overview
- **Confidence**: 0.99
- **Coverage**: 100% parsed & validated

---

**Red AgentTeam | 2026-04-15 22:45 GMT+8**


## 相關文檔

- [[devtools-overview]]
- [[devtools-overview.capsules]]
