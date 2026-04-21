# Nano 文檔驗證報告

**驗證日期:** 2026-04-20  
**來源 URL:** https://www.nano-editor.org/docs.php  
**可信度:** 0.99 ✅  
**證據等級:** 原文 + 實測

---

## ✅ 已驗證事實 (3 個)

| 事實 | 內容 | 驗證命令 | 可信度 |
|------|------|---------|--------|
| **手冊** | `man nano` 查看官方手冊 | `man nano` | 0.99 |
| **幫助** | `nano --help` 顯示選項 | `nano --help` | 0.99 |
| **配置** | `~/.nanorc` 用戶配置路徑 | 文檔確認 | 0.99 |

---

## ⚠️ 候選事實 (3 個)

- 交互式 ^G 幫助 (0.90)
- .nanorc 語法高亮 (0.90)
- FAQ 全文 (0.88)

---

## 📦 固化資產

- **Genes:** `gene_nano_man`, `gene_nano_cli_help`, `gene_nanorc_check`
- **Capsule:** `capsule_nano_env_check`

---

**trust_level:** 🟢 llm+verified  
**verified_by:** RedAgentTeam  
**verification_method:** 原文對照 + 命令行實測
