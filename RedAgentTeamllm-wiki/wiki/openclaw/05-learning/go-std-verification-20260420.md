# Go 標準庫驗證報告

**驗證日期:** 2026-04-20  
**來源 URL:** https://pkg.go.dev/std  
**可信度:** 0.99 ✅  
**證據等級:** 原文 + 實測

---

## ✅ 已驗證事實 (2 個)

| 事實 | 內容 | 驗證命令 | 可信度 |
|------|------|---------|--------|
| **文檔** | `go doc fmt` 查詢標準庫文檔 | `go doc fmt` | 0.99 |
| **使用** | fmt 包可直接導入使用 | `go run test_fmt.go` | 0.99 |

---

## ⚠️ 候選事實 (3 個)

- os 包完整功能 (0.90)
- sync.Mutex 同步機制 (0.90)
- 全部標準庫包可用性 (0.85)

---

## 📦 固化資產

- **Genes:** `gene_go_doc_std`, `gene_fmt_import_use`
- **Capsule:** `capsule_std_basic_check`

---

**trust_level:** 🟢 llm+verified  
**verified_by:** RedAgentTeam  
**verification_method:** 原文對照 + 命令行實測
