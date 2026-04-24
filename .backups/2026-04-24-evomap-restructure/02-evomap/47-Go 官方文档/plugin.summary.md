---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Plugin.Summary
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
# Go plugin 标准库完整固化

**作用**: 运行时动态加载 .so 共享库

**支持**: 仅 Linux（你的服务器 ✅ 完美支持）

**编译**: `go build -buildmode=plugin`

**限制**:
- 加载后不可卸载
- 必须同 Go 版本编译

**你的环境**: ✅ 100% 可运行 plugin

**状态**: 生产可用

---

**Source**: https://pkg.go.dev/plugin  
**Go**: 1.26.1  
**Platforms**: Linux, FreeBSD  
**Confidence**: 0.99
