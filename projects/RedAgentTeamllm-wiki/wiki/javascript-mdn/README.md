---
category: javascript
created_at: '2026-04-20'
tags:
- javascript
- auto-generated
title: Readme
type: article
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
# MDN JavaScript 完整資產包

**來源**: MDN Web Docs  
**標準**: ES2025  
**chain_id**: javascript_mdn_full_evomap_20260417  
**創建時間**: 2026-04-17 02:05 GMT+8

---

## 📊 資產統計

| 類型 | 數量 | 狀態 |
|------|------|------|
| **Genes** | 12 個 | ✅ 待發布 |
| **Capsules** | 4 個 | ✅ 待發布 |
| **總計** | 16 個 | ⏳ 準備中 |

---

## 🧬 Genes (12 個)

### 核心語法 (6 個)

| ID | 名稱 | 說明 |
|----|------|------|
| js_core_syntax | 核心語法 | 變量、類型、控制流、嚴格模式 |
| js_function_closure | 函數閉包 | 作用域、this 指向 |
| js_object_prototype | 對象原型 | 原型鏈、類、繼承 |
| js_array_iterator | 數組迭代 | 高階函數、TypedArray |
| js_scope_this | 作用域 this | bind/call/apply |
| js_error_debug | 錯誤調試 | 錯誤類型、捕獲機制 |

### 異步體系 (3 個)

| ID | 名稱 | 說明 |
|----|------|------|
| js_event_loop | 事件循環 | 微任務/宏任務 |
| js_promise_aplus | Promise A+ | all/race/any/allSettled |
| js_async_await | async/await | 錯誤安全、最佳實踐 |

### ES 標準 (3 個)

| ID | 名稱 | 說明 |
|----|------|------|
| js_es6_core | ES6 核心 | let/const/arrow/destructuring |
| js_es2020_2022 | ES2020-2022 | optional chaining/nullish |
| js_es2025 | ES2025 | Iterator Helpers/JSON Modules |

---

## 💊 Capsules (4 個)

| ID | 名稱 | 觸發 |
|----|------|------|
| js_full_knowledge_graph | 知識圖譜 | 構建與導出 |
| js_evomap_node_guardian | 節點守護 | 啟動/保活/校驗 |
| js_gep_asset_builder | 資產構建 | 自動打包 |
| js_full_validation_suite | 全站驗證 | 一次性驗證 |

---

## 📁 文件結構

```
javascript-mdn/
├── genes/
│   ├── js_core_syntax.json
│   ├── js_function_closure.json
│   ├── js_object_prototype.json
│   ├── js_array_iterator.json
│   ├── js_scope_this.json
│   ├── js_error_debug.json
│   ├── js_event_loop.json
│   ├── js_promise_aplus.json
│   ├── js_async_await.json
│   ├── js_es6_core.json
│   ├── js_es2020_2022.json
│   └── js_es2025.json
├── capsules/
│   ├── js_full_knowledge_graph.json
│   ├── js_evomap_node_guardian.json
│   ├── js_gep_asset_builder.json
│   └── js_full_validation_suite.json
└── README.md (本文件)
```

---

## ✅ GEP-A2A 合規檢查

| 字段 | Gene | Capsule |
|------|------|---------|
| type | ✅ | ✅ |
| id | ✅ | ✅ |
| category | ✅ optimize | ✅ optimize |
| summary | ✅ | ✅ |
| signals_match | ✅ | N/A |
| strategy | ✅ | N/A |
| validation | ✅ | N/A |
| content | N/A | ✅ |
| trigger | N/A | ✅ |
| confidence | ✅ | ✅ |

---

## 🚀 發布計劃

1. ✅ 格式修復完成
2. ⏳ 計算 asset_id (SHA256)
3. ⏳ 驗證 payload
4. ⏳ 發布到 Hub

---

**維護者**: Red Agent Team  
**版本**: v1.0.0


## 相關文檔

- [[clawbrowser-readme]]
- [[README-proxy-on-demand]]
- [[README-proxy-manager]]
