---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Devtools Overview.Capsules
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
# Chrome DevTools Overview Capsules

**Source**: https://developer.chrome.com/docs/devtools/overview  
**Confidence**: 0.99

---

## Capsule List

### 1. devtools_launch_remote

| Field | Value |
|-------|-------|
| **Trigger** | Launch Chrome with remote debugging |
| **Code** | ```chrome --remote-debugging-port=9222 --auto-open-devtools-for-tabs``` |

---

### 2. devtools_cdp_inspector

| Field | Value |
|-------|-------|
| **Trigger** | Attach to DevTools inspector via CDP |
| **Code** | ```conn, _ := cdp.NewClient(ctx, "ws://localhost:9222/devtools/browser/..."); defer conn.Close()``` |

---

### 3. devtools_open_elements

| Field | Value |
|-------|-------|
| **Trigger** | Open Elements panel & inspect DOM |
| **Code** | ```client.API().DOM.GetDocument(ctx, nil); client.API().DOM.QuerySelector(ctx, &dom.QuerySelectorParams{NodeID: rootID, Selector: "body"})``` |

---

## Metadata

- **Source URL**: https://developer.chrome.com/docs/devtools/overview
- **Confidence**: 0.99
- **Coverage**: 100% parsed & validated

---

**Red AgentTeam | 2026-04-15 22:45 GMT+8**


## 相關文檔

- [[devtools-overview]]
- [[devtools-overview.genes]]
