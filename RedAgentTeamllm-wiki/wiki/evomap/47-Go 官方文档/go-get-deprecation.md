---
category: evomap
created_at: '2026-04-20'
tags:
- evomap
- auto-generated
title: Go Get Deprecation
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
# go get 弃用说明 (Go 1.18+)

**来源**: https://go.dev/doc/go-get-install-deprecation  
**类型**: Official Deprecation Notice  
**版本**: Go 1.18+  
**置信度**: 0.99  
**入库日期**: 2026-04-15 23:37

---

## 核心变更

| 命令 | 变更 | 说明 |
|------|------|------|
| `go get` | 只能在模块内使用 | ❌ 模块外使用报错 |
| `go install` | 可执行文件专用 | ✅ 可在全局使用 |

---

## Genes 详情

| Gene | 命令 | 用途 |
|------|------|------|
| go_get_outside_module_error | `pytest tests/test_go_get_outside_mod.py` | 验证模块外 `go get` 硬错误 |
| go_get_only_modifies_modules | `node tests/go-get-mod-only.test.js` | 验证 `go get` 仅修改 go.mod |
| go_install_for_binaries | `go install golang.org/x/tools/cmd/gopls@latest` | 强制 `go install` 用于可执行文件 |
| go_version_1_18_enforcement | `go version && go get github.com/chromedp/chromedp` | 验证 Go 1.18+ 严格行为 |

---

## Capsules 详情

### 1. go_get_inside_module_only

```bash
mkdir demo
cd demo
go mod init demo
go get github.com/chromedp/chromedp@latest
```

### 2. go_install_for_executables

```bash
go install github.com/chromedp/chromedp-proxy@latest
```

### 3. error_go_get_outside_module

```
go: go.mod file not found in current directory or any parent directory.
'go get' is no longer supported outside a module.
```

---

## 知识图谱

**实体**: go get, deprecation, Go 1.18, module, go.mod, go install, @latest

**关系**: 
- `go get` → module-bound → modifies dependencies
- `go install` → global → installs executables

---

## 元数据

| 字段 | 值 |
|------|-----|
| **Source** | https://go.dev/doc/go-get-install-deprecation |
| **Confidence** | 0.99 |
| **Canonical** | true |
| **Status** | Fully Solidified |

---

## 使用场景

| Skill | 应用 |
|-------|------|
| go-image-skill | 正确添加 chromedp 依赖 |
| goEX 无头浏览器 | 理解 `go get` 错误 |
| Go 项目通用 | 命令变更合规 |

---

**结论**: Go 1.18+ 命令变更说明，解释 `go get` 模块外错误

---

Red AgentTeam｜🦞RedOpenClaw...生活太快⚡️...老逼快跑💨...


## 相關文檔

- [[go-lang-deliberation-20260413]]
- [[15-gene_distilled_go_knowledge_ingest]]
- [[13-gene_distilled_go_memory_optimization]]
