---
category: self-research-assets
created_at: '2026-04-22'
tags:
- self-research
- assets
- data
- reports
title: 自研项目数据资产索引
type: index
version: '1.0.0'
---

# 自研项目数据资产索引

**最后更新**: 2026-04-22  
**维护者**: Red Agent Team  
**版本**: v1.0.0

---

## 🎯 定位

存放自研项目的**原始数据资产**（报告 + 数据），与基因库配合使用。

**基因库**: `../genes/` - 设计思想、演化记录、数据基因  
**资产库**: 本报告 - 原始报告、测试数据、开发日志

---

## 📊 资产概览

| 类别 | 文件数 | 代表资产 |
|------|--------|---------|
| **测试报告** | 8+ | 1 亿次测试、v0.5.0 测试 |
| **事故报告** | 8+ | P0 事故完整复盘 |
| **开发日志** | 3+ | meeting-log, plugin-dev-log |
| **优化报告** | 2+ | OPTIMIZATION_* |
| **基准数据** | 3 | CSV/JSON 测试数据 |

---

## 📁 目录结构

```
assets/
├── index.md                  # 本索引
├── reports/
│   ├── test/                 # 测试报告
│   │   ├── goEX-50 遍推演报告.md
│   │   ├── goEX-100K-test.md
│   │   ├── goEX-100M-test.md (1 亿次)
│   │   ├── OPTIMIZATION_EVALUATION.md
│   │   ├── goEX-full-test-report-20260422.md
│   │   └── ...
│   ├── accident/             # 事故报告
│   │   ├── accident-report-20260422.md
│   │   ├── accident-escalation-20260422.md
│   │   ├── ... (8 份事故报告)
│   │   └── closing-summary-20260422.md
│   └── dev-logs/             # 开发日志
│       ├── meeting-log-20260422.md
│       ├── plugin-dev-log-20260422.md
│       └── sync-log-20260422.md
└── data/
    └── benchmarks/           # 基准数据
        ├── goEX-v0.5.0-benchmark.json
        └── goToken-baseline.json
```

---

## 🧬 基因关联

### goEX 数据基因

| 基因编码 | 数据 | 位置 |
|---------|------|------|
| `goEX_data_001` | 1 亿次测试数据 | `../genes/goEX/100M-test-gene.md` |
| `goEX_data_002` | 事故完整数据 | `../genes/goEX/accident-data-gene.md` |
| `goEX_data_003` | v0.5.0 测试数据 | `../genes/goEX/v0.5.0-test-gene.md` |

### goToken 数据基因

| 基因编码 | 数据 | 位置 |
|---------|------|------|
| `goToken_data_001` | 75% 命中率数据 | `../genes/goToken/75pct-hitrate-gene.md` |

---

## 📝 使用说明

### 引用数据资产

**格式**:
```markdown
参考 goEX 1 亿次测试报告 [goEX_data_001]
位置：assets/reports/test/goEX-100M-test.md
```

### 查找数据

1. **按类型** → 查看 `reports/test/`、`reports/accident/` 等目录
2. **按基因编码** → 查看 `../genes/` 中的基因文档
3. **按索引** → 使用本索引文档

---

## 🔗 相关链接

| 链接 | 说明 |
|------|------|
| [基因库](../genes/) | 设计思想、演化记录 |
| [项目索引](../index.md) | 自研项目总索引 |
| [goEX 代码](../../../goEX/) | goEX 源代码 |
| [goToken 代码](../../../goToken/) | goToken 源代码 |

---

**最后更新**: 2026-04-22  
**状态**: ✅ 创建完成
