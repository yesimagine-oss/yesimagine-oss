# Go 測試框架驗證報告

**驗證日期:** 2026-04-20  
**來源 URL:** https://go.dev/doc/tutorial/add-a-test  
**可信度:** 0.99 ✅  
**證據等級:** 原文 + 實測

---

## ✅ 已驗證事實 (4 個)

| 事實 | 內容 | 驗證命令 | 可信度 |
|------|------|---------|--------|
| **單元測試** | `go test` 運行測試 | `go test ./...` | 0.99 |
| **覆蓋率** | `go test -cover` 分析覆蓋率 | `go test -cover` | 0.99 |
| **基準測試** | `go test -bench` 性能基準 | `go test -bench=.` | 0.99 |
| **詳細輸出** | `go test -v` 詳細日誌 | `go test -v` | 0.99 |

---

## 📦 固化資產

- **Genes:** 4 個 (test/cover/bench/verbose)
- **Capsule:** 1 個 (完整測試流程)

---

**trust_level:** 🟢 llm+verified  
**verified_by:** RedAgentTeam  
**verification_method:** 原文對照 + 命令行實測
