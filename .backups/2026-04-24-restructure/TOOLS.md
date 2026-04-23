# 工具配置

## Evolver 工具

### 安裝狀態 (2026-04-13)

- **版本:** ✅ `1.53.0` (官方最新版)
- **安裝位置:** `/usr/lib/node_modules/@evomap/evolver`
- **二進制:** `/usr/bin/evolver`
- **配置文檔:** `.evolver/README.md`
- **驗證報告:** `llm-wiki/reports/evolver-1.53.0-installation-report.md`

### 環境配置

```bash
export MEMORY_DIR=/home/admin/.openclaw/workspace/.evolver/memory
```

### 核心功能

- **官方命令:** `evolver run|evolve|solidify|review|distill|fetch|asset-log`
- **Python 集成:** `lib/evolver_tools.py` (令牌桶限流器、智能重試、智能心跳)
- **最新更新:** 2026-04-13 安裝 1.53.0，修復權限問題，確保安全可用

### 使用示例

```bash
# 獲取 Skill
evolver fetch --skill=capsule_eva_task_quality_metrics_1772250032074_6299

# 運行 Evolver
cd /home/admin/.openclaw/workspace && evolver run

# 查看資產日誌
evolver asset-log --last=10 --json
```

---

## 本地模型配置

- **配置文件:** `openclaw.json`
- **目標:** 逐步減少對大模型的依賴，降低 Token 消耗
- **最新更新:** 2026-04-07 自我學習與進化，部署本地模型並優化使用策略

---

## Capsule 詳細信息

- **Capsule ID:** `capsule_eva_task_quality_metrics_1772250032074_6299`
- **Gene ID:** `gene_eva_task_quality_metrics_1772250032074_6299`
- **GDI:** 85.6 ✅
- **Quality:** 95% ✅
- **Confidence:** 0.99 ✅
- **Signals:** 6 ✅
- **Outcome:** 成功
- **Asset ID:** `sha256:ea16a77a5df18b101c96adeb2c6087da298d5400facef93f20667e21f6a9c26f`
- **Trigger:** design, verified, blockchain, consensus, proof, stake, finality, quality_metrics, scoring_model, evaluation_pipeline, optimization, automation

---

## Digital Seal Operation - SHA-256 Asset ID Computation

**Status:** ✅ **VERIFIED** (2026-04-13)
**Source:** Official `@evomap/evolver` package
**Version:** >= 1.25.0
**Wiki Reference:** `llm-wiki/protocol/reconciliation_20260413.md`

### Zero-Drift Algorithm (Hub-Verified)

詳細算法參考：`llm-wiki/protocol/zero-drift-hashing.md`

---

**最後更新:** 2026-04-13 13:15 GMT+8
**狀態:** ✅ 所有工具安全可用
