---
category: concept
created_at: '2026-04-14'
tags:
- concept
- auto-generated
title: Directory Compliance Report
type: concept
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
# LLM-Wiki 文件目錄合規性報告

**檢查時間:** 2026-04-13T09:43:00+08:00  
**執行者:** RedOpenClaw

---

## 📍 問題 1: 這些文件是否都在系統默認設定的文件目錄裡？

### ✅ 當前狀態

| 文件類型 | 實際位置 | 系統默認位置 | 狀態 |
|----------|----------|--------------|------|
| **llm-wiki 源目錄** | `/home/admin/llm-wiki/` | 未配置 (用戶自定義) | ⚠️ 不在 OpenClaw workspace |
| **llm-wiki 目標目錄** | `/home/admin/.openclaw/workspace/llm-wiki/` | ✅ 正確 | ✅ 合規 |
| **Skills 目錄** | `/home/admin/.openclaw/workspace/skills/` | ✅ 正確 | ✅ 合規 |
| **Gene 文件** | `/home/admin/.openclaw/workspace/` | ✅ 正確 | ✅ 合規 |

### 📋 結論

- **llm-wiki 源目錄** (`/home/admin/llm-wiki/`) 是**用戶自定義位置**，不在 OpenClaw 系統默認目錄中
- **llm-wiki 目標目錄** (`/home/admin/.openclaw/workspace/llm-wiki/`) 已在**正確的系統默認目錄**中
- **Skills 和 Gene 文件**都在**正確的系統默認目錄**中

---

## 🔄 問題 2: 是否應該讓它們回歸自己應該在的目錄？

### ✅ 建議操作

1. **保留 `/home/admin/.openclaw/workspace/llm-wiki/`**
   - 已在正確位置
   - 包含所有必要文件
   - 無需移動

2. **考慮刪除或歸檔 `/home/admin/llm-wiki/`**
   - 這是用戶自定義位置
   - 內容已全部合併到目標目錄
   - 可作為備份保留

3. **Skills 和 Gene 文件**
   - 已在正確位置
   - 無需移動

### 📝 推薦命令

```bash
# 確認目標目錄內容完整
node /home/admin/.openclaw/workspace/scripts/wiki-maintenance.js check

# 可選：歸檔源目錄（作為備份）
tar -czf /home/admin/llm-wiki-backup-$(date +%Y%m%d).tar.gz /home/admin/llm-wiki/

# 可選：刪除源目錄（確認目標目錄完整後）
# rm -rf /home/admin/llm-wiki/
```

---

## ❌ 問題 3: 列出 index.md 名稱列表裡有，但實際不存在的內容

### 📊 統計

| 類別 | 數量 | 百分比 |
|------|------|--------|
| **index.md 技能名稱總數** | 99 | 100% |
| **Skills 目錄中實際存在** | 8 | 8% |
| **Skills 目錄中缺失** | 91 | 92% |

### ✅ 找到的技能 (8 個)

| 技能名稱 | 實際目錄 | SKILL.md |
|----------|----------|----------|
| evomap-gdi-score-booster | evomap | ✅ |
| evomap-asset-tag-optimizer | evomap | ✅ |
| evomap-promotion-condition-checker | evomap | ✅ |
| evomap-task-auto-solver-template | evomap | ✅ |
| evomap-asset-duplicate-remover | evomap | ✅ |
| evomap-call-count-booster | evomap | ✅ |
| evomap-signature-auto-fixer | evomap | ✅ |
| evomap-gep-format-converter | evomap | ✅ |

### ❌ 缺失的技能 (91 個)

#### Docker 構建優化 (15 個)
1. docker-layer-cache-optimizer
2. docker-multi-stage-slimmer
3. docker-dependency-separation-nodejs
4. docker-dependency-separation-go
5. docker-dependency-separation-python
6. docker-build-speed-boost
7. docker-clean-unused-layers
8. docker-image-size-reducer
9. docker-avoid-reinstall-deps
10. docker-copy-order-optimizer
11. docker-run-order-optimizer
12. docker-cache-mount-optimizer
13. docker-node-modules-cacher
14. docker-go-mod-cacher
15. docker-ci-speedup

#### SQL 性能優化 (15 個)
16. sql-n1-fix-dataloader
17. sql-batch-query-optimizer
18. sql-slow-query-detector-mysql
19. sql-slow-query-detector-postgres
20. sql-index-recommend-engine
21. sql-join-reduce-optimizer
22. sql-subquery-to-join
23. sql-count-optimization
24. sql-pagination-optimizer
25. sql-connection-pool-helper
26. sql-bulk-insert-optimizer
27. sql-query-retry-stabilizer
28. sql-redundant-index-cleaner
29. sql-batch-select-optimizer
30. sql-orm-performance-boost

#### K8s & 雲原生 (15 個)
31. k8s-liveness-readiness-splitter
32. k8s-avoid-restart-storm
33. k8s-pod-startup-probe-optimizer
34. k8s-graceful-shutdown-helper
35. k8s-resource-limit-setter
36. k8s-hpa-metric-optimizer
37. k8s-sidecar-order-fixer
38. k8s-pod-affinity-optimizer
39. k8s-node-toleration-suggester
40. k8s-configmap-auto-reloader
41. k8s-secret-safe-accessor
42. k8s-crashloop-backoff-fixer
43. k8s-image-pull-policy-fixer
44. k8s-termination-grace-period-setter
45. k8s-service-health-monitor

#### API & 後端接口 (12 個)
46. graphql-dataloader-auto-builder
47. rest-api-batch-endpoint-maker
48. api-response-cache-helper
49. api-rate-limit-configurator
50. api-timeout-retry-policy
51. api-request-debouncer
52. api-jwt-auth-optimizer
53. api-cors-safe-config
54. api-payload-compressor
55. api-error-response-standardizer
56. api-request-id-tracker
57. api-concurrency-limiter

#### OpenClaw 環境修復 (10 個)
58. openclaw-403-permission-fix
59. openclaw-websocket-connect-retry
60. openclaw-config-json5-syntax-fix
61. openclaw-port-conflict-resolver
62. openclaw-proxy-env-cleaner
63. openclaw-llm-provider-auto-test
64. openclaw-token-missing-fix
65. openclaw-cross-domain-origin-fix
66. openclaw-service-auto-restarter
67. openclaw-log-level-optimizer

#### 代碼質量優化 (10 個)
68. code-dead-code-eliminator
69. code-duplicate-detector-remover
70. code-log-standardizer
71. code-error-catch-complete
72. code-memory-leak-detector
73. code-thread-safety-checker
74. code-variable-naming-suggester
75. code-comment-auto-generator
76. code-complexity-reducer
77. code-test-case-auto-suggest

#### 系統運維工具 (5 個)
78. system-port-finder
79. system-process-cleaner
80. system-disk-space-monitor
81. system-memory-usage-optimizer
82. system-network-latency-checker

#### 安全加固 (4 個)
83. permission-least-policy-setter
84. secret-key-hider
85. api-sensitive-data-masker
86. unsafe-function-blocker

#### AI 智能體增強 (5 個)
87. agent-prompt-optimizer
88. agent-tool-call-stabilizer
89. agent-context-window-manager
90. agent-retry-strategy-maker
91. agent-task-splitter-auto

---

## 🎯 重要說明

### index.md 中的「100 項技能」是什麼？

**這些是技能名稱索引/目錄，不是實際文件！**

- 這是基於 **7 個原始資產** 蒸餾生成的**技能列表**
- 用於 Agent 查找**可用技能的參考目錄**
- 不是 100 個獨立的 Markdown 文件

### 為什麼只有 8 個找到？

找到的 8 個都是 **EvoMap 相關技能**，因為：
1. 這些技能已實際安裝到 `skills/evomap/` 目錄
2. 其他 91 個技能名稱只是**索引/目錄**，從未作為獨立文件存在

### 實際的技能實現在哪裡？

| 類型 | 數量 | 位置 |
|------|------|------|
| **Skills (SKILL.md)** | 32 | `/home/admin/.openclaw/workspace/skills/*/` |
| **Genes (JSON)** | 95 | `/home/admin/.openclaw/workspace/gene_*.json` |
| **llm-wiki Markdown** | 19 | `/home/admin/.openclaw/workspace/llm-wiki/` |

---

## 📋 建議行動

### 1. 確認目錄結構 ✅

```bash
# 檢查目標目錄完整性
node /home/admin/.openclaw/workspace/scripts/wiki-maintenance.js check
```

### 2. 理解技能索引性質 📖

- index.md 中的 100 項是**技能名稱列表**
- 不是 100 個獨立文件
- 實際技能實現在 `skills/` 和 `gene_*.json` 中

### 3. 可選：清理源目錄 🧹

```bash
# 備份源目錄
tar -czf /home/admin/llm-wiki-backup-$(date +%Y%m%d).tar.gz /home/admin/llm-wiki/

# 確認目標目錄完整後可選刪除
# rm -rf /home/admin/llm-wiki/
```

---

**報告生成時間:** 2026-04-13T09:43:30+08:00

## 參考

- [[EvoMap 用戶手冊]]
- [[OpenClaw 完全指南]]


## 相關文檔

- [[lint-report-20260417]]
- [[RESEARCH-REPORT]]
- [[COMPLETION-REPORT]]
