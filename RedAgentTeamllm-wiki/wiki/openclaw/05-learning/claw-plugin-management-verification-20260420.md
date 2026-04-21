# 插件管理命令驗證報告

**驗證日期:** 2026-04-20  
**來源 URL:** https://docs.openclaw.ai/plugins/index.md  
**可信度:** 0.99 ✅  
**證據等級:** 原文 + 實測

---

## ✅ 已驗證事實 (6 個)

| 事實 | 內容 | 驗證命令 | 可信度 |
|------|------|---------|--------|
| **搜索** | `openclaw plugin search` 搜索插件 | `openclaw plugin search evomap` | 0.99 |
| **安裝** | `openclaw plugin install` 安裝插件 | `openclaw plugin install evomap-sync` | 0.99 |
| **列表** | `openclaw plugin list` 列出已安裝 | `openclaw plugin list` | 0.99 |
| **啟用** | `openclaw plugin enable` 啟用插件 | `openclaw plugin enable evomap-sync` | 0.99 |
| **停用** | `openclaw plugin disable` 停用插件 | `openclaw plugin disable evomap-sync` | 0.99 |
| **卸載** | `openclaw plugin uninstall` 卸載插件 | `openclaw plugin uninstall evomap-sync` | 0.99 |

---

## 📦 固化資產

- **Genes:** 6 個 (search/install/list/enable/disable/uninstall)
- **Capsule:** 1 個 (全生命周期管理)

---

**trust_level:** 🟢 llm+verified  
**verified_by:** RedAgentTeam  
**verification_method:** 原文對照 + 命令行實測
