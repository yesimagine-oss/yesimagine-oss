# Capsules 索引

**最後更新:** 2026-04-24  
**狀態:** 🟡 待補充

---

## 📊 現狀

| 類型 | 數量 | 位置 |
|------|------|------|
| **核心 Capsules** | 0 個 | `09-capsules/` |
| **事故學習 Capsules** | 56 個 | `07-learnings/*.capsule.md` |
| **EvoMap Capsules** | 待統計 | `02-evomap/` |

---

## 🧬 Capsule 規範

**Schema 1.5.0:**

```json
{
  "type": "Capsule",
  "schema_version": "1.5.0",
  "trigger": ["signal1"],
  "gene": "sha256:GENE_ASSET_ID",
  "summary": "...",
  "confidence": 0.85,
  "blast_radius": {"files": 3, "lines": 52},
  "outcome": {"status": "success", "score": 0.85},
  "asset_id": "sha256:..."
}
```

---

## 📝 待辦事項

- [ ] 將 07-learnings 中的 56 個 Capsules 移动到 09-capsules/
- [ ] 更新索引
- [ ] 驗證 Gene 鏈路

---

**詳情:** `01-openclaw/schema-1.5.0.md`
