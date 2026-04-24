---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Gin.Genes
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
# Gene: gin_module_validate

**Summary**: Verify Gin is installed in go.mod

**Command**:
```bash
go list -m github.com/gin-gonic/gin
```

---

# Gene: gin_route_functional_check

**Summary**: Validate GET/POST routes work

**Command**:
```bash
go test -v gin_route_test.go
```

---

# Gene: gin_json_binding_validate

**Summary**: Test JSON auto-binding & validation

**Command**:
```bash
pytest tests/test_gin_json_bind.py
```

---

# Gene: gin_server_startup_check

**Summary**: Test server starts on port 8080

**Command**:
```bash
go run main.go & curl http://localhost:8080/ping
```
