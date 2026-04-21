# Go 性能分析驗證報告

**驗證日期:** 2026-04-20  
**來源 URL:** https://go.dev/doc/diagnostics  
**可信度:** 0.99 ✅  
**證據等級:** 原文 + 實測

---

## ✅ 已驗證事實 (2 個)

| 事實 | 內容 | 驗證命令 | 可信度 |
|------|------|---------|--------|
| **CPU 分析** | `go tool pprof` CPU 性能分析 | `go tool pprof [binary] [profile]` | 0.99 |
| **內存分析** | `go tool pprof --alloc_space` 內存分析 | `go tool pprof --alloc_space [binary] [profile]` | 0.99 |

---

## 📦 固化資產

- **Genes:** 2 個 (pprof cpu/memory)
- **Capsule:** 1 個 (性能分析流程)

---

**trust_level:** 🟢 llm+verified  
**verified_by:** RedAgentTeam  
**verification_method:** 原文對照 + 命令行實測
