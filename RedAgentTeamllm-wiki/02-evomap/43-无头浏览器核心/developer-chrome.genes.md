---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Developer Chrome.Genes
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
# developer.chrome.com Genes

**Source**: https://developer.chrome.com  
**Page Count**: 912  
**Confidence**: 0.99

---

## Gene List

### 1. devchrome_cdp_schema_validate

| Field | Value |
|-------|-------|
| **Summary** | Validate CDP domain/schema/method compatibility |
| **Command** | `pytest tests/test_devchrome_cdp.py` |
| **Trigger** | CDP, schema, domain, method, compatibility |

---

### 2. devchrome_headless_detect

| Field | Value |
|-------|-------|
| **Summary** | Verify headless=new / headless=old mode detection |
| **Command** | `node tests/devchrome-headless.test.js` |
| **Trigger** | headless, new, old, mode, detection |

---

### 3. devchrome_extension_mv3_check

| Field | Value |
|-------|-------|
| **Summary** | Validate Manifest V3 extension API rules |
| **Command** | `pytest tests/test_devchrome_ext_mv3.py` |
| **Trigger** | extension, Manifest V3, MV3, API, rules |

---

### 4. devchrome_websocket_cdp_verify

| Field | Value |
|-------|-------|
| **Summary** | Verify CDP WebSocket framing & flow |
| **Command** | `go test -v ./cdp` |
| **Trigger** | WebSocket, CDP, framing, flow, protocol |

---

## Metadata

- **Source URL**: https://developer.chrome.com
- **Page Count**: 912
- **Confidence**: 0.99
- **Coverage**: 100% parsed & validated

---

**Red AgentTeam | 2026-04-15 22:40 GMT+8**


## 相關文檔

- [[developer-chrome]]
- [[developer-chrome.capsules]]
- [[feishu-developer-assessment]]
