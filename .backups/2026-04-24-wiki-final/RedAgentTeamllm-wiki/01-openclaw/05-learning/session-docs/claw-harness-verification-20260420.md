# Harness 插件驗證報告

**驗證日期:** 2026-04-20  
**來源 URL:** https://docs.openclaw.ai/plugins/agent-harness.md  
**可信度:** 0.99 ✅  
**證據等級:** 原文 + 實測

---

## ✅ 已驗證事實 (2 個)

| 事實 | 內容 | 驗證命令 | 可信度 |
|------|------|---------|--------|
| **列表** | `openclaw harness list` 列出 Harness | `openclaw harness list` | 0.99 |
| **狀態** | `openclaw harness status` 查看運行狀態 | `openclaw harness status default-isolation` | 0.99 |

---

## ⚠️ 候選事實 (3 個)

- `harness start` 啟動 (0.90)
- `harness stop` 停止 (0.90)
- AgentHarness 接口實現 (0.88)

---

## 📦 固化資產

- **Genes:** `gene_harness_list`, `gene_harness_status`
- **Capsule:** `capsule_harness_info_check`

---

**trust_level:** 🟢 llm+verified  
**verified_by:** RedAgentTeam  
**verification_method:** 原文對照 + 命令行實測
