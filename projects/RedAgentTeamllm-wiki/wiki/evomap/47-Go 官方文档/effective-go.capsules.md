---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Effective Go.Capsules
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
# Effective Go Capsules

**Source**: https://go.dev/doc/effective_go  
**Confidence**: 0.99

---

## Capsule List

### 1. effective_go_basic_idiom

| Field | Value |
|-------|-------|
| **Trigger** | Idiomatic Go structure |
| **Code** | ```package main; import "fmt"; func main() { s := "Effective Go"; fmt.Println(s) }``` |

---

### 2. effective_go_interface_composition

| Field | Value |
|-------|-------|
| **Trigger** | Small, composable interfaces |
| **Code** | ```type Stringer interface { String() string }``` |

---

### 3. effective_go_goroutine_channel

| Field | Value |
|-------|-------|
| **Trigger** | Idiomatic concurrency |
| **Code** | ```ch := make(chan int); go func() { ch <- 1 }(); <-ch``` |

---

## Metadata

- **Source URL**: https://go.dev/doc/effective_go
- **Confidence**: 0.99
- **Coverage**: 100% parsed & validated

---

**Red AgentTeam | 2026-04-15 22:54 GMT+8**


## 相關文檔

- [[effective-go]]
- [[effective-go.genes]]
