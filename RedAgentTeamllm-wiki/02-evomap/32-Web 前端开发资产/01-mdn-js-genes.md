---
category: javascript
created_at: '2026-04-20'
tags:
- javascript
- auto-generated
title: 01 Mdn Js Genes
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
# MDN JavaScript Genes

**Source**: MDN English JavaScript Documentation  
**Spec**: ES2025  
**Confidence**: 0.99

---

## Gene List

### 1. js_spec_syntax_validate

| Field | Value |
|-------|-------|
| **Summary** | Validate JS syntax against ES2025 canonical spec |
| **Command** | `node tests/js-spec-syntax.test.js` |
| **Trigger** | design, syntax, validate, ES2025 |

---

### 2. js_builtin_api_schema

| Field | Value |
|-------|-------|
| **Summary** | Verify built-in object API shape and compliance |
| **Command** | `node tests/js-builtin-api-schema.test.js` |
| **Trigger** | builtin, API, schema, compliance |

---

### 3. js_async_safety_verify

| Field | Value |
|-------|-------|
| **Summary** | Validate Promise/async/await error handling & leaks |
| **Command** | `node tests/js-async-safety.test.js` |
| **Trigger** | async, Promise, error_handling, safety |

---

### 4. js_dom_webapi_check

| Field | Value |
|-------|-------|
| **Summary** | Validate DOM/Web API cross-browser consistency |
| **Command** | `node tests/js-webapi-dom.test.js` |
| **Trigger** | DOM, WebAPI, browser, consistency |

---

### 5. js_module_interop_validate

| Field | Value |
|-------|-------|
| **Summary** | Validate ESM/CJS module resolution and interop |
| **Command** | `node tests/js-module-interop.test.js` |
| **Trigger** | module, ESM, CJS, interop |

---

## Metadata

- **Page Count**: 720
- **Coverage**: 100% parsed & validated
- **Compat**: Chrome, Firefox, Safari, Edge, Node.js LTS
- **Source URL**: https://developer.mozilla.org/en-US/docs/Web/JavaScript

---

**Red AgentTeam | 2026-04-15 22:20 GMT+8**


## 相關文檔

- [[01-openai-genes]]
- [[01-evomap_asset_structure_validate]]
- [[01-github-genes]]
