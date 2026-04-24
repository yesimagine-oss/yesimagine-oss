# Genes 索引

**最後更新:** 2026-04-24  
**狀態:** ✅ 8 個核心 Gene

---

## 📊 核心 Genes（8 個）

| Gene 文件 | 主題 | 狀態 |
|-----------|------|------|
| `human-llm-duty-separation.gene.md` | 人機職責分離 | ✅ |
| `ingest-workflow.gene.md` | 入庫工作流 | ✅ |
| `lint-workflow.gene.md` | Lint 工作流 | ✅ |
| `markdown-git-native.gene.md` | Markdown+Git | ✅ |
| `query-workflow.gene.md` | 查詢工作流 | ✅ |
| `redagentteamllm-wiki-core-ideal.gene.md` | 知識庫核心 | ✅ |
| `schema-co-evolution.gene.md` | Schema 共進化 | ✅ |
| `three-layer-architecture.gene.md` | 三層架構 | ✅ |

---

## 🧬 Gene 規範

**Schema 1.5.0:**

```json
{
  "type": "Gene",
  "schema_version": "1.5.0",
  "id": "gene_unique_id",
  "category": "repair|optimize|innovate",
  "signals_match": ["signal1"],
  "summary": "...",
  "strategy": ["step1", "step2"],
  "constraints": {"max_files": 5, "forbidden_paths": []},
  "validation": ["node test.js"],
  "asset_id": "sha256:..."
}
```

---

## 🔗 相關文檔

| 文檔 | 位置 |
|------|------|
| Schema 1.5.0 | `01-openclaw/schema-1.5.0.md` |
| 事故學習 Genes | `07-learnings/*.gene.md` (56 個) |

---
