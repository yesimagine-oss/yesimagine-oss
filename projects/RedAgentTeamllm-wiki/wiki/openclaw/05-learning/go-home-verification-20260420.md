# Go 官網驗證報告

**驗證日期:** 2026-04-20  
**來源 URL:** https://go.dev  
**可信度:** 0.99 ✅  
**證據等級:** 原文 + 實測

---

## ✅ 已驗證事實 (3 個)

| 事實 | 內容 | 驗證命令 | 可信度 |
|------|------|---------|--------|
| **版本** | `go version` 查詢版本 | `go version` | 0.99 |
| **運行** | `go run` 執行最小程序 | `go run hello.go` | 0.99 |
| **環境** | `go env` 查看編譯環境 | `go env GOOS GOARCH` | 0.99 |

---

## ⚠️ 候選事實 (3 個)

- Go 完整語言規範 (0.90)
- Go 並發原語 (0.92)
- 標準庫完整可用性 (0.90)

---

## 📦 固化資產

- **Genes:** `gene_go_version_check`, `gene_go_run_hello`, `gene_go_env_check`
- **Capsule:** `capsule_go_env_quick_check`

---

**trust_level:** 🟢 llm+verified  
**verified_by:** RedAgentTeam  
**verification_method:** 原文對照 + 命令行實測
