---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Plugin.Capsules
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
# Capsule: plugin_so_build

**Trigger**: 编译插件（Linux only）

**Code**:
```go
// plugin.go (export func/variable)
package main
func Hello() string { return "from plugin" }
```

**Compile**:
```bash
go build -buildmode=plugin -o my.so plugin.go
```

---

# Capsule: plugin_load_and_call

**Trigger**: 主程序加载并调用插件

**Code**:
```go
p, _ := plugin.Open("my.so")
f, _ := p.Lookup("Hello")
fmt.Println(f.(func() string)())
```

---

# Capsule: plugin_linux_only_guard

**Trigger**: 系统检查（官方约束）

**Code**:
```go
if runtime.GOOS != "linux" {
 log.Fatal("plugin only supports Linux")
}
```
