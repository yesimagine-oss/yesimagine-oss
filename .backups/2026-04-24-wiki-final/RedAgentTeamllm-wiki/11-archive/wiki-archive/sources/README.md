---
category: sources
created_at: '2026-04-15T06:59:33+08:00'
tags:
- sources
- 來源頁面索引
title: 知识来源索引
type: index
version: '1.0'

# Provenance
provenance:
  source_url: "internal"
  captured_at: "2026-04-20"
  verified_by: "Red Agent Team"
  verification_method: "auto"
  trust_score: 0.95

# Trust Boundary
trust_level: "llm+verified"
evidence_level: "原文 + 實測"
---
# 來源頁面索引

**最後更新:** 2026-04-14  
**狀態:** ✅ 已激活

---

## 📋 什麼是來源頁面？

來源頁面 (Sources) 記錄知識的**原始來源**，包括：

- 📄 文檔鏈接
- 🔗 URL 引用
- 📚 參考資料
- 🎥 視頻/音頻來源
- 💬 對話記錄

---

## 🎯 來源頁面的作用

1. **可追溯** - 每個知識都有來源
2. **可驗證** - 可以回溯原始信息
3. **可更新** - 來源變化時可以更新
4. **可共享** - 他人可以查找原始資料

---

## 📁 來源頁面結構

```
sources/
├── README.md           # 本索引文件
├── 2026-04-14-github-llm-wiki-maintenance.md  # 來源總結
├── 2026-04-13-openclaw-docs.md
└── ...
```

---

## 📝 來源頁面模板

```markdown
---
title: "來源標題"
type: "source"
source_url: "https://..."
source_type: "documentation|article|video|conversation"
captured_at: "2026-04-14"
tags: ["標籤 1", "標籤 2"]
---

# 來源總結

## 原始內容

[記錄原始內容或摘要]

## 相關知識

- [[相關實體]]
- [[相關概念]]

## 備註

[任何額外說明]
```

---

## ✅ 來源頁面清單

| 文件 | 來源類型 | 捕獲時間 |
|------|---------|---------|
| (待創建) | - | - |

---

**維護者:** Red Agent Team  
**協議:** LLM Wiki Mode v1.0


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]
