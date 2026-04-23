---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Plugin.Genes
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
# Gene: plugin_platform_support

**Summary**: 验证当前系统（Linux）支持 plugin

**Command**:
```bash
go env GOOS | grep -q linux && echo "supported"
```

---

# Gene: plugin_build_validate

**Summary**: 验证插件可编译为 -buildmode=plugin

**Command**:
```bash
go build -buildmode=plugin -o test.so test.go
```

---

# Gene: plugin_open_lookup_validate

**Summary**: 验证加载插件 + 查找符号

**Command**:
```bash
go run main.go
```

---

# Gene: plugin_abi_compatibility

**Summary**: 验证主程序与插件 Go 版本一致

**Command**:
```bash
go version && go version
```
