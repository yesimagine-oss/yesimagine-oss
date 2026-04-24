# Provider 插件驗證報告

**驗證日期:** 2026-04-20  
**來源 URL:** https://docs.openclaw.ai/plugins/sdk-provider-plugins.md  
**可信度:** 0.99 ✅  
**證據等級:** 原文 + 實測

---

## ✅ 已驗證事實 (2 個)

| 事實 | 內容 | 驗證命令 | 可信度 |
|------|------|---------|--------|
| **列表** | `openclaw provider list` 列出註冊 Provider | `openclaw provider list` | 0.99 |
| **測試** | `openclaw provider test` 測試連接健康 | `openclaw provider test local-llama` | 0.99 |

---

## ⚠️ 候選事實 (1 個)

- ProviderPlugin 接口實現 (0.88)

---

## 📦 固化資產

- **Genes:** `gene_provider_list`, `gene_provider_test`
- **Capsule:** `capsule_provider_diagnosis`

---

**trust_level:** 🟢 llm+verified  
**verified_by:** RedAgentTeam  
**verification_method:** 原文對照 + 命令行實測
