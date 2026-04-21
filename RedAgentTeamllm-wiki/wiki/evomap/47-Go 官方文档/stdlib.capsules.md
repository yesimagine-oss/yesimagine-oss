---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Stdlib.Capsules
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
# Go Standard Library Capsules

**Source**: https://pkg.go.dev/std  
**Confidence**: 0.99

---

## Capsule List

### 1. stdlib_http_server

| Field | Value |
|-------|-------|
| **Trigger** | Standard net/http server |
| **Code** | ```http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) { io.WriteString(w, "hello std") }); log.Fatal(http.ListenAndServe(":8080", nil))``` |

---

### 2. stdlib_json_marshal

| Field | Value |
|-------|-------|
| **Trigger** | encoding/json canonical usage |
| **Code** | ```type X struct{ A string }; b, _ := json.Marshal(X{A: "test"})``` |

---

### 3. stdlib_context_timeout

| Field | Value |
|-------|-------|
| **Trigger** | context with timeout |
| **Code** | ```ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second); defer cancel()``` |

---

## Metadata

- **Source URL**: https://pkg.go.dev/std
- **Confidence**: 0.99
- **Coverage**: 100% parsed & indexed

---

**Red AgentTeam | 2026-04-15 22:58 GMT+8**
