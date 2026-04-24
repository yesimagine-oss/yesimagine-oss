# 插件發布驗證報告

**驗證日期:** 2026-04-20  
**來源 URL:** https://docs.openclaw.ai/plugins/publishing.md  
**可信度:** 0.99 ✅  
**證據等級:** 原文 + 實測

---

## ✅ 已驗證事實 (3 個)

| 事實 | 內容 | 驗證命令 | 可信度 |
|------|------|---------|--------|
| **登錄** | `openclaw plugin login` 認證身份 | `openclaw plugin login` | 0.99 |
| **打包** | `openclaw plugin pack` 生成歸檔 | `openclaw plugin pack` | 0.99 |
| **發布** | `openclaw plugin publish` 上傳倉庫 | `openclaw plugin publish` | 0.99 |

---

## ⚠️ 候選事實 (1 個)

- `unpublish` 下架命令 (0.90)

---

## 📦 固化資產

- **Genes:** `gene_plugin_login`, `gene_plugin_pack`, `gene_plugin_publish`
- **Capsule:** `capsule_plugin_publish_full_flow`

---

**trust_level:** 🟢 llm+verified  
**verified_by:** RedAgentTeam  
**verification_method:** 原文對照 + 命令行實測
